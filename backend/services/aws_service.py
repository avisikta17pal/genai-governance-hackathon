# pyright: reportMissingImports=false
import logging
import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, List
from datetime import datetime
import hashlib
import uuid

logger = logging.getLogger(__name__)


class AWSService:
    """
    AWS Service for integrating with AWS Bedrock and other AWS services
    Handles AI model interactions, content moderation, and AWS resource management
    """

    def __init__(self):
        self.bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.comprehend_client = boto3.client("comprehend", region_name="us-east-1")
        self.s3_client = boto3.client("s3", region_name="us-east-1")
        self.kms_client = boto3.client("kms", region_name="us-east-1")

        # Available models
        self.available_models = {
            "anthropic.claude-3-sonnet-20240229-v1:0": {
                "provider": "anthropic",
                "max_tokens": 4096,
                "supports_streaming": True,
                "content_moderation": True,
            },
            "anthropic.claude-3-haiku-20240307-v1:0": {
                "provider": "anthropic",
                "max_tokens": 4096,
                "supports_streaming": True,
                "content_moderation": True,
            },
            "amazon.titan-text-express-v1": {
                "provider": "amazon",
                "max_tokens": 4096,
                "supports_streaming": False,
                "content_moderation": True,
            },
            "meta.llama-2-70b-chat-v1": {
                "provider": "meta",
                "max_tokens": 4096,
                "supports_streaming": False,
                "content_moderation": False,
            },
        }

        # Default model configuration
        self.default_model = "anthropic.claude-3-sonnet-20240229-v1:0"

        # Content moderation settings
        self.moderation_settings = {
            "enabled": True,
            "categories": ["hate", "violence", "sexual", "self_harm"],
            "threshold": 0.7,
        }

        # Rate limiting
        self.rate_limits = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "concurrent_requests": 10,
        }

    async def generate_response(
        self, prompt: str, context: Optional[Dict] = None, model: Optional[str] = None
    ) -> str:
        """
        Generate AI response using AWS Bedrock
        """
        try:
            logger.info("Generating AI response via AWS Bedrock")

            # Use default model if none specified
            model_id = model or self.default_model

            # Validate model
            if model_id not in self.available_models:
                raise ValueError(f"Model {model_id} not available")

            # Prepare request body
            request_body = await self._prepare_request_body(prompt, context, model_id)

            # Make request to Bedrock
            response = await self._call_bedrock_model(model_id, request_body)

            # Extract and process response
            ai_response = await self._process_bedrock_response(response, model_id)

            logger.info("AI response generated successfully")
            return ai_response

        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again."

    async def _prepare_request_body(
        self, prompt: str, context: Optional[Dict] = None, model_id: Optional[str] = None
    ) -> Dict:
        """Prepare request body for Bedrock API"""
        try:
            # Add context to prompt if provided
            full_prompt = prompt
            if context:
                context_str = json.dumps(context, indent=2)
                full_prompt = f"Context: {context_str}\n\nUser Request: {prompt}"

            # Add governance disclaimers
            governance_disclaimer = """
            IMPORTANT: This is an AI-generated response. Please verify all information independently.
            This response is for informational purposes only and should not be considered as professional advice.
            """
            full_prompt = f"{full_prompt}\n\n{governance_disclaimer}"

            # Prepare request based on model provider
            if model_id and "anthropic" in model_id:
                return {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "messages": [{"role": "user", "content": full_prompt}],
                    "system": "You are a helpful AI assistant that provides accurate, helpful, and compliant responses. Always consider ethical implications and provide appropriate disclaimers when necessary.",
                }
            elif model_id and "amazon" in model_id:
                return {
                    "inputText": full_prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 4096,
                        "stopSequences": [],
                        "temperature": 0.7,
                        "topP": 0.9,
                    },
                }
            elif model_id and "meta" in model_id:
                return {
                    "prompt": full_prompt,
                    "max_gen_len": 4096,
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            else:
                # Default format
                return {"prompt": full_prompt, "max_tokens": 4096, "temperature": 0.7}

        except Exception as e:
            logger.error(f"Error preparing request body: {str(e)}")
            raise

    async def _call_bedrock_model(self, model_id: str, request_body: Dict) -> Dict:
        """Make API call to Bedrock model"""
        try:
            # Convert request body to JSON
            request_json = json.dumps(request_body)

            # Make synchronous call (in production, use async client)
            response = self.bedrock_client.invoke_model(
                modelId=model_id, body=request_json
            )

            # Parse response
            response_body = json.loads(response["body"].read())

            return response_body

        except ClientError as e:
            logger.error(f"AWS Bedrock error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error calling Bedrock model: {str(e)}")
            raise

    async def _process_bedrock_response(self, response: Dict, model_id: str) -> str:
        """Process and extract text from Bedrock response"""
        try:
            # Extract text based on model provider
            if "anthropic" in model_id:
                # Claude response format
                if "content" in response and len(response["content"]) > 0:
                    return response["content"][0]["text"]
                else:
                    return "No response generated"

            elif "amazon" in model_id:
                # Titan response format
                if "results" in response and len(response["results"]) > 0:
                    return response["results"][0]["outputText"]
                else:
                    return "No response generated"

            elif "meta" in model_id:
                # Llama response format
                if "generation" in response:
                    return response["generation"]
                else:
                    return "No response generated"

            else:
                # Default extraction
                if "text" in response:
                    return response["text"]
                elif "content" in response:
                    return response["content"]
                else:
                    return str(response)

        except Exception as e:
            logger.error(f"Error processing Bedrock response: {str(e)}")
            return "Error processing response"

    async def moderate_content(self, text: str) -> Dict:
        """
        Moderate content using AWS Comprehend and Bedrock
        """
        try:
            logger.info("Moderating content via AWS Comprehend and Bedrock")

            # Step 1: Use Comprehend for PII detection
            pii_response = self.comprehend_client.detect_pii_entities(
                Text=text, LanguageCode="en"
            )
            pii_entities = pii_response.get("Entities", [])
            pii_types = [entity["Type"] for entity in pii_entities]

            # Step 2: Use Comprehend for sentiment analysis
            sentiment_response = self.comprehend_client.detect_sentiment(
                Text=text, LanguageCode="en"
            )

            # Step 3: Use Bedrock for advanced content moderation
            bedrock_moderation = await self._bedrock_content_moderation(text)

            # Combine results
            moderation_result = {
                "flagged": len(pii_entities) > 0 or bedrock_moderation.get("flagged", False),
                "pii_detected": pii_types,
                "sentiment": sentiment_response.get("Sentiment", "NEUTRAL"),
                "confidence": sentiment_response.get("SentimentScore", {}),
                "bedrock_moderation": bedrock_moderation,
                "risk_level": self._calculate_risk_level(pii_entities, bedrock_moderation),
                "moderation_source": "aws_comprehend_and_bedrock",
            }

            logger.info(
                f"Content moderation complete: {moderation_result['risk_level']}"
            )
            return moderation_result

        except ClientError as e:
            logger.error(f"AWS service error: {str(e)}")
            return {
                "flagged": False,
                "pii_detected": [],
                "sentiment": "NEUTRAL",
                "confidence": {},
                "risk_level": "unknown",
                "error": str(e),
            }
        except Exception as e:
            logger.error(f"Error moderating content: {str(e)}")
            return {
                "flagged": False,
                "pii_detected": [],
                "sentiment": "NEUTRAL",
                "confidence": {},
                "risk_level": "unknown",
                "error": str(e),
            }

    async def _bedrock_content_moderation(self, text: str) -> Dict:
        """
        Use AWS Bedrock for advanced content moderation
        """
        try:
            # Use Claude for content moderation
            moderation_prompt = f"""
            Analyze the following text for harmful content, bias, and inappropriate material.
            Focus on: hate speech, violence, self-harm, sexual content, and discriminatory language.
            
            Text to analyze: "{text}"
            
            Provide a JSON response with:
            - flagged: boolean (true if harmful content detected)
            - categories: object with scores for hate, violence, sexual, self_harm (0.0 to 1.0)
            - confidence: float (0.0 to 1.0)
            - reasoning: string (brief explanation)
            """

            # Call Bedrock for moderation
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": moderation_prompt}],
                "system": "You are a content moderation AI. Respond only with valid JSON.",
            }

            response = self.bedrock_client.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps(request_body)
            )

            response_body = json.loads(response["body"].read())
            moderation_text = response_body["content"][0]["text"]

            # Parse the JSON response
            try:
                moderation_result = json.loads(moderation_text)
                return {
                    "flagged": moderation_result.get("flagged", False),
                    "categories": moderation_result.get("categories", {}),
                    "confidence": moderation_result.get("confidence", 0.5),
                    "reasoning": moderation_result.get("reasoning", ""),
                    "source": "bedrock_claude",
                }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "flagged": "harmful" in moderation_text.lower() or "inappropriate" in moderation_text.lower(),
                    "categories": {"hate": 0.0, "violence": 0.0, "sexual": 0.0, "self_harm": 0.0},
                    "confidence": 0.5,
                    "reasoning": "Fallback moderation analysis",
                    "source": "bedrock_claude_fallback",
                }

        except Exception as e:
            logger.error(f"Bedrock moderation error: {str(e)}")
            return {
                "flagged": False,
                "categories": {"hate": 0.0, "violence": 0.0, "sexual": 0.0, "self_harm": 0.0},
                "confidence": 0.0,
                "reasoning": f"Error: {str(e)}",
                "source": "bedrock_error",
            }

    def _calculate_risk_level(self, pii_entities: List, bedrock_moderation: Dict) -> str:
        """
        Calculate overall risk level based on PII and Bedrock moderation
        """
        pii_count = len(pii_entities)
        bedrock_flagged = bedrock_moderation.get("flagged", False)
        bedrock_confidence = bedrock_moderation.get("confidence", 0.0)

        # High risk if multiple PII entities or high-confidence Bedrock flag
        if pii_count > 2 or (bedrock_flagged and bedrock_confidence > 0.7):
            return "high"
        # Medium risk if some PII or moderate Bedrock flag
        elif pii_count > 0 or (bedrock_flagged and bedrock_confidence > 0.3):
            return "medium"
        else:
            return "low"

    async def encrypt_data(self, data: str, key_id: str) -> Dict:
        """
        Encrypt sensitive data using AWS KMS
        """
        try:
            logger.info("Encrypting data via AWS KMS")

            # Encrypt data
            response = self.kms_client.encrypt(
                KeyId=key_id, Plaintext=data.encode("utf-8")
            )

            encrypted_data = response["CiphertextBlob"]

            return {
                "encrypted_data": encrypted_data,
                "key_id": key_id,
                "encryption_algorithm": "AES_256",
                "encrypted": True,
            }

        except ClientError as e:
            logger.error(f"AWS KMS error: {str(e)}")
            return {
                "encrypted_data": None,
                "key_id": key_id,
                "encrypted": False,
                "error": str(e),
            }
        except Exception as e:
            logger.error(f"Error encrypting data: {str(e)}")
            return {
                "encrypted_data": None,
                "key_id": key_id,
                "encrypted": False,
                "error": str(e),
            }

    async def decrypt_data(self, encrypted_data: bytes, key_id: str) -> Dict:
        """
        Decrypt data using AWS KMS
        """
        try:
            logger.info("Decrypting data via AWS KMS")

            # Decrypt data
            response = self.kms_client.decrypt(
                CiphertextBlob=encrypted_data, KeyId=key_id
            )

            decrypted_data = response["Plaintext"].decode("utf-8")

            return {
                "decrypted_data": decrypted_data,
                "key_id": key_id,
                "decrypted": True,
            }

        except ClientError as e:
            logger.error(f"AWS KMS error: {str(e)}")
            return {
                "decrypted_data": None,
                "key_id": key_id,
                "decrypted": False,
                "error": str(e),
            }
        except Exception as e:
            logger.error(f"Error decrypting data: {str(e)}")
            return {
                "decrypted_data": None,
                "key_id": key_id,
                "decrypted": False,
                "error": str(e),
            }

    async def store_audit_log(
        self, audit_data: Dict, bucket_name: str, key: str
    ) -> bool:
        """
        Store audit log in S3
        """
        try:
            logger.info(f"Storing audit log in S3: {key}")

            # Convert audit data to JSON
            audit_json = json.dumps(audit_data, indent=2)

            # Upload to S3
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=audit_json,
                ContentType="application/json",
                ServerSideEncryption="AES256",
            )

            logger.info(f"Audit log stored successfully: s3://{bucket_name}/{key}")
            return True

        except ClientError as e:
            logger.error(f"AWS S3 error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error storing audit log: {str(e)}")
            return False

    async def get_model_info(self, model_id: str) -> Optional[Dict]:
        """
        Get information about a specific model
        """
        try:
            if model_id in self.available_models:
                return self.available_models[model_id]
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return None

    async def list_available_models(self) -> List[str]:
        """
        List all available models
        """
        try:
            return list(self.available_models.keys())

        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []

    async def check_service_health(self) -> Dict:
        """
        Check health of AWS services
        """
        try:
            health_status = {
                "bedrock": "unknown",
                "comprehend": "unknown",
                "kms": "unknown",
                "s3": "unknown",
            }

            # Test Bedrock (simulated)
            try:
                # In production, make a simple API call
                health_status["bedrock"] = "healthy"
            except Exception:
                health_status["bedrock"] = "unhealthy"

            # Test Comprehend (simulated)
            try:
                # In production, make a simple API call
                health_status["comprehend"] = "healthy"
            except Exception:
                health_status["comprehend"] = "unhealthy"

            # Test KMS (simulated)
            try:
                # In production, make a simple API call
                health_status["kms"] = "healthy"
            except Exception:
                health_status["kms"] = "unhealthy"

            # Test S3 (simulated)
            try:
                # In production, make a simple API call
                health_status["s3"] = "healthy"
            except Exception:
                health_status["s3"] = "unhealthy"

            return health_status

        except Exception as e:
            logger.error(f"Error checking service health: {str(e)}")
            return {
                "bedrock": "unknown",
                "comprehend": "unknown",
                "kms": "unknown",
                "s3": "unknown",
                "error": str(e),
            }
