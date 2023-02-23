from flask import Blueprint, jsonify, request
import pika
import app.config as config

api = Blueprint('api', __name__)

# Producer endpoint
@api.route('/publish', methods=['POST'])
def publish():
    """
    Publlish a new message
    ---
    parameters:
        -   name: body
            in: body
            required: true
            description: The message needed to publish.
            schema:      # Request body contents
              type: object
              properties:
                message:
                  type: string
                  required: true
                
    responses:
        200:
            description: Message published
        400:
            description: No message provided
    """
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        credentials=pika.PlainCredentials(
            username=config.RABBITMQ_USERNAME,
            password=config.RABBITMQ_PASSWORD,
        ),
    ))
    channel = connection.channel()

    # Declare the exchange and queue
    channel.exchange_declare(
        exchange=config.RABBITMQ_EXCHANGE,
        exchange_type='direct',
    )
    channel.queue_declare(queue=config.RABBITMQ_QUEUE)
    channel.queue_bind(queue=config.RABBITMQ_QUEUE, exchange=config.RABBITMQ_EXCHANGE)

    # Publish the message
    channel.basic_publish(
        exchange=config.RABBITMQ_EXCHANGE,
        routing_key=config.RABBITMQ_QUEUE,
        body=message,
    )

    connection.close()

    return jsonify({'success': True}), 200

# Consumer endpoint
@api.route('/consume', methods=['GET'])
def consume():
    """
    Consume a new message
    ---
    responses:
        200:
          description: Message consumed
    """
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        credentials=pika.PlainCredentials(
            username=config.RABBITMQ_USERNAME,
            password=config.RABBITMQ_PASSWORD,
        ),
    ))
    channel = connection.channel()

    # Declare the exchange and queue
    channel.exchange_declare(
        exchange=config.RABBITMQ_EXCHANGE,
        exchange_type='direct',
    )
    channel.queue_declare(queue=config.RABBITMQ_QUEUE)
    channel.queue_bind(queue=config.RABBITMQ_QUEUE, exchange=config.RABBITMQ_EXCHANGE)

    # Consume a message
    method, properties, body = channel.basic_get(queue=config.RABBITMQ_QUEUE)
    if method is None:
        return jsonify({'message': None}), 200

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)

    connection.close()

    return jsonify({'message': body.decode()}), 200
