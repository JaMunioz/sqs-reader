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
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

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
            try:
                bucket_name = 'copus-audio'
                s3_object_key = str(message['Body'])
                
                s3.head_object(Bucket=bucket_name, Key=s3_object_key)
                print(f"El objeto '{s3_object_key}' fue encontrado.")
            except:
                print(f"No existe un objeto '{s3_object_key}'.")
            
            """
            Aqui se procesa un audio
            """

            # Elimina el mensaje de la cola después de procesarlo (comentarlo si no quieres eliminar los mensajes)
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    else:
        print('No se encontraron mas mensajes en la cola, se procedera a cerrar el cluster')
        lambda_function_name = 'deleteAudioProcessDeploy'
        lambda_client = boto3.client('lambda', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
        try:
            # Ejecuta la función Lambda
            response = lambda_client.invoke(
                FunctionName=lambda_function_name,
                InvocationType='RequestResponse'  # Puedes cambiar el tipo de invocación según tus necesidades
            )

            # Verifica la respuesta
            if response['StatusCode'] == 200:
                print(f"Función Lambda '{lambda_function_name}' ejecutada correctamente")
            else:
                print(f"Error al ejecutar la función Lambda: {response}")
        except Exception as e:
            print(f"Error al ejecutar la función Lambda: {e}")

        break

