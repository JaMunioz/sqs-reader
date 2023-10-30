import boto3
import time
import os
from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_session_token = None 
queue_name = 'audio-proc-queue'
region_name = 'us-east-1' 

# Configura el cliente de SQS
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token,region_name=region_name)

# Obtiene la URL de la cola
response = sqs.get_queue_url(QueueName=queue_name)
queue_url = response['QueueUrl']


while True:
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

    # Procesa los mensajes
    if 'Messages' in response:
        for message in response['Messages']:
            body = message['Body']
            receipt_handle = message['ReceiptHandle']

            # Haz algo con el cuerpo del mensaje aquí
            print(f'Mensaje recibido: {body}')
            time.sleep(5)

            # Elimina el mensaje de la cola después de procesarlo (comentarlo si no quieres eliminar los mensajes)
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    else:
        print('No se encontraron mas mensajes en la cola')
        break

