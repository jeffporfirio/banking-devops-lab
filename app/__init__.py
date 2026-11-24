from flask import Flask, jsonify, request
from app.database import get_collection, get_database
from app.logging_config import configure_logging


def create_app():
    configure_logging()
    app = Flask(__name__)
    logger = app.logger
    logger.info("Banking API application initialized")

    @app.get("/health")
    @app.get("/health/live")
    def health():
        return jsonify({
            "status": "ok",
            "service": "banking_api"
        }), 200

    @app.get("/health/ready")
    def readiness():
        try:
            get_database().command("ping")

            logger.info("Readiness check successful: MongoDB connected")

            return jsonify({
                "status": "ready",
                "service": "banking_api",
                "database": "connected"
            }), 200

        except Exception:
            logger.exception("Readiness check failed: MongoDB unavailable")

            return jsonify({
                "status": "not_ready",
                "service": "banking_api",
                "database": "unavailable"
            }), 503

    @app.get("/transactions")
    def list_transactions():
        logger.info("Fetching transactions")

        collection = get_collection()

        transactions = list(
            collection.find({}, {"_id": 0})
        )

        logger.info(
            "Transactions retrieved successfully: count=%d",
            len(transactions)
        )

        return jsonify(transactions), 200

    @app.post("/transactions")
    def create_transaction():
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            logger.warning("Transaction rejected: JSON object required")

            return jsonify({
                "error": "JSON object required"
            }), 400

        required_fields = {"reference", "amount"}

        if not required_fields.issubset(payload):
            logger.warning("Transaction rejected: required fields missing")
            return jsonify({
                "error": "reference and amount are required"
            }), 400

        reference = payload["reference"]
        amount = payload["amount"]

        if not isinstance(reference, str) or not reference.strip():
            logger.warning("Transaction rejected: invalid reference")

            return jsonify({
                "error": "reference must be a non-empty string"
            }), 400

        if (
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
            or amount <= 0
        ):
            logger.warning("Transaction rejected: invalid amount")

            return jsonify({
                "error": "amount must be a positive number"
            }), 400

        collection = get_collection()

        collection.insert_one({
            "reference": reference,
            "amount": amount
        })

        logger.info("Transaction created successfully")

        return jsonify({
            "message": "Transaction created"
        }), 201

    return app
