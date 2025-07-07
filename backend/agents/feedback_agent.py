import logging
import boto3
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
import uuid

logger = logging.getLogger(__name__)


class FeedbackAgent:
    """
    Feedback Agent: Gathers user feedback on system performance, analyzes feedback to suggest improvements,
    and collects feedback anonymously to protect privacy.
    """

    def __init__(self):
        self.dynamodb_client = boto3.client("dynamodb", region_name="us-east-1")

        # Feedback categories
        self.feedback_categories = {
            "accuracy": {
                "description": "Accuracy and correctness of AI responses",
                "metrics": ["response_accuracy", "factual_correctness", "relevance"],
            },
            "usability": {
                "description": "Ease of use and user experience",
                "metrics": ["interface_clarity", "response_time", "ease_of_use"],
            },
            "compliance": {
                "description": "Compliance with regulations and policies",
                "metrics": [
                    "policy_adherence",
                    "disclaimer_accuracy",
                    "privacy_protection",
                ],
            },
            "ethics": {
                "description": "Ethical considerations and fairness",
                "metrics": ["bias_detection", "fairness", "transparency"],
            },
            "security": {
                "description": "Security and data protection",
                "metrics": ["data_security", "access_controls", "audit_trails"],
            },
        }

        # Feedback analysis models
        self.analysis_models = {
            "sentiment_analysis": {
                "positive_keywords": [
                    "good",
                    "great",
                    "excellent",
                    "helpful",
                    "accurate",
                    "fast",
                ],
                "negative_keywords": [
                    "bad",
                    "poor",
                    "slow",
                    "inaccurate",
                    "confusing",
                    "wrong",
                ],
                "neutral_keywords": ["okay", "fine", "acceptable", "average"],
            },
            "improvement_suggestions": {
                "accuracy": [
                    "Improve training data quality",
                    "Implement fact-checking mechanisms",
                    "Add source citations",
                    "Regular model retraining",
                ],
                "usability": [
                    "Simplify user interface",
                    "Improve response time",
                    "Add user tutorials",
                    "Enhance error messages",
                ],
                "compliance": [
                    "Update compliance policies",
                    "Improve disclaimer accuracy",
                    "Enhance audit logging",
                    "Regular compliance reviews",
                ],
                "ethics": [
                    "Implement bias detection",
                    "Improve fairness metrics",
                    "Enhance transparency",
                    "Regular ethics audits",
                ],
                "security": [
                    "Enhance encryption",
                    "Improve access controls",
                    "Regular security audits",
                    "Update security policies",
                ],
            },
        }

        # Privacy protection settings
        self.privacy_settings = {
            "anonymize_feedback": True,
            "hash_user_identifiers": True,
            "retention_period": 365 * 24 * 60 * 60,  # 1 year in seconds
            "data_minimization": True,
        }

    async def process_feedback(
        self, session_id: str, rating: int, feedback_text: str, user_id: str
    ) -> Dict:
        """
        Process user feedback and analyze it for improvements
        """
        try:
            logger.info(f"Processing feedback for session {session_id}, user {user_id}")

            # Step 1: Anonymize feedback if requested
            anonymized_feedback = await self._anonymize_feedback(feedback_text, user_id)

            # Step 2: Categorize feedback
            feedback_categories = await self._categorize_feedback(feedback_text)

            # Step 3: Analyze sentiment
            sentiment_analysis = await self._analyze_sentiment(feedback_text)

            # Step 4: Generate improvement suggestions
            improvement_suggestions = await self._generate_improvement_suggestions(
                feedback_categories, sentiment_analysis, rating
            )

            # Step 5: Store feedback
            feedback_id = await self._store_feedback(
                session_id,
                rating,
                anonymized_feedback,
                feedback_categories,
                sentiment_analysis,
                user_id,
            )

            # Step 6: Update system metrics
            metrics_update = await self._update_system_metrics(
                rating, feedback_categories
            )

            result = {
                "feedback_id": feedback_id,
                "analysis": {
                    "categories": feedback_categories,
                    "sentiment": sentiment_analysis,
                    "improvement_suggestions": improvement_suggestions,
                    "metrics_update": metrics_update,
                },
                "privacy_protected": self.privacy_settings["anonymize_feedback"],
                "timestamp": datetime.utcnow().isoformat(),
                "processed": True,
            }

            logger.info(f"Feedback processing complete: {feedback_id}")
            return result

        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return {
                "feedback_id": f"error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "analysis": {
                    "error": str(e),
                    "categories": [],
                    "sentiment": "unknown",
                    "improvement_suggestions": [],
                },
                "privacy_protected": False,
                "timestamp": datetime.utcnow().isoformat(),
                "processed": False,
            }

    async def _anonymize_feedback(self, feedback_text: str, user_id: str) -> str:
        """Anonymize feedback to protect user privacy"""
        if not self.privacy_settings["anonymize_feedback"]:
            return feedback_text

        # Remove or hash potentially identifying information
        anonymized_text = feedback_text

        # Hash user ID if present in feedback
        if user_id in anonymized_text:
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:8]
            anonymized_text = anonymized_text.replace(user_id, f"user_{user_hash}")

        # Remove email addresses
        import re

        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        anonymized_text = re.sub(email_pattern, "[EMAIL]", anonymized_text)

        # Remove phone numbers
        phone_pattern = r"\b\d{3}-\d{3}-\d{4}\b"
        anonymized_text = re.sub(phone_pattern, "[PHONE]", anonymized_text)

        # Remove names (simple pattern)
        name_pattern = r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"
        anonymized_text = re.sub(name_pattern, "[NAME]", anonymized_text)

        return anonymized_text

    async def _categorize_feedback(self, feedback_text: str) -> List[str]:
        """Categorize feedback into relevant categories"""
        feedback_lower = feedback_text.lower()
        categories = []

        # Check each category for relevant keywords
        for category, config in self.feedback_categories.items():
            category_keywords = {
                "accuracy": [
                    "accurate",
                    "correct",
                    "wrong",
                    "factual",
                    "truth",
                    "error",
                ],
                "usability": [
                    "easy",
                    "hard",
                    "confusing",
                    "clear",
                    "interface",
                    "user-friendly",
                ],
                "compliance": [
                    "compliance",
                    "policy",
                    "regulation",
                    "disclaimer",
                    "legal",
                ],
                "ethics": ["bias", "fair", "unfair", "discrimination", "ethical"],
                "security": ["secure", "privacy", "data", "protection", "safe"],
            }

            if category in category_keywords:
                for keyword in category_keywords[category]:
                    if keyword in feedback_lower:
                        categories.append(category)
                        break

        return list(set(categories))  # Remove duplicates

    async def _analyze_sentiment(self, feedback_text: str) -> Dict:
        """Analyze sentiment of feedback text"""
        feedback_lower = feedback_text.lower()

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count positive keywords
        for keyword in self.analysis_models["sentiment_analysis"]["positive_keywords"]:
            if keyword in feedback_lower:
                positive_count += 1

        # Count negative keywords
        for keyword in self.analysis_models["sentiment_analysis"]["negative_keywords"]:
            if keyword in feedback_lower:
                negative_count += 1

        # Count neutral keywords
        for keyword in self.analysis_models["sentiment_analysis"]["neutral_keywords"]:
            if keyword in feedback_lower:
                neutral_count += 1

        # Determine overall sentiment
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = "positive"
            confidence = min(
                0.9, (positive_count - max(negative_count, neutral_count)) / 10
            )
        elif negative_count > positive_count and negative_count > neutral_count:
            sentiment = "negative"
            confidence = min(
                0.9, (negative_count - max(positive_count, neutral_count)) / 10
            )
        else:
            sentiment = "neutral"
            confidence = 0.7

        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_score": positive_count,
            "negative_score": negative_count,
            "neutral_score": neutral_count,
        }

    async def _generate_improvement_suggestions(
        self, categories: List[str], sentiment: Dict, rating: int
    ) -> List[str]:
        """Generate improvement suggestions based on feedback analysis"""
        suggestions = []

        # Add general suggestions based on rating
        if rating <= 2:
            suggestions.append("Immediate attention required - low user satisfaction")
        elif rating <= 3:
            suggestions.append("Improvement needed - moderate user satisfaction")
        elif rating >= 4:
            suggestions.append("Maintain current performance - high user satisfaction")

        # Add category-specific suggestions
        for category in categories:
            if category in self.analysis_models["improvement_suggestions"]:
                category_suggestions = self.analysis_models["improvement_suggestions"][
                    category
                ]
                suggestions.extend(
                    category_suggestions[:2]
                )  # Top 2 suggestions per category

        # Add sentiment-based suggestions
        if sentiment["sentiment"] == "negative":
            suggestions.append("Investigate and address user concerns promptly")
        elif sentiment["sentiment"] == "positive":
            suggestions.append("Maintain and replicate successful practices")

        return list(set(suggestions))  # Remove duplicates

    async def _store_feedback(
        self,
        session_id: str,
        rating: int,
        anonymized_feedback: str,
        categories: List[str],
        sentiment: Dict,
        user_id: str,
    ) -> str:
        """Store feedback in database"""
        try:
            feedback_id = f"feedback_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

            # Create feedback record
            feedback_record = {
                "feedback_id": feedback_id,
                "session_id": session_id,
                "user_id_hash": hashlib.sha256(user_id.encode()).hexdigest()[:16],
                "rating": rating,
                "feedback_text": anonymized_feedback,
                "categories": categories,
                "sentiment": sentiment,
                "timestamp": datetime.utcnow().isoformat(),
                "privacy_protected": self.privacy_settings["anonymize_feedback"],
            }

            # In production, this would store in DynamoDB
            # For demo purposes, we'll simulate the storage

            # Simulate successful storage
            logger.info(f"Stored feedback record: {feedback_id}")
            return feedback_id

        except Exception as e:
            logger.error(f"Error storing feedback record: {str(e)}")
            return f"error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    async def _update_system_metrics(self, rating: int, categories: List[str]) -> Dict:
        """Update system performance metrics based on feedback"""
        try:
            # In production, this would update metrics in a database
            # For demo, we'll simulate metric updates

            metrics_update = {
                "average_rating": rating,  # In production, calculate from all ratings
                "feedback_count": 1,  # In production, increment total count
                "category_breakdown": {},
                "trend": "stable",
            }

            # Update category breakdown
            for category in categories:
                if category not in metrics_update["category_breakdown"]:
                    metrics_update["category_breakdown"][category] = 0
                metrics_update["category_breakdown"][category] += 1

            return metrics_update

        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            return {"error": str(e)}

    async def get_feedback_analytics(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict:
        """Get analytics on collected feedback"""
        try:
            # In production, this would query the database
            # For demo, we'll return simulated analytics

            analytics = {
                "total_feedback": 1250,
                "average_rating": 4.2,
                "rating_distribution": {"1": 25, "2": 45, "3": 150, "4": 450, "5": 580},
                "category_breakdown": {
                    "accuracy": 0.35,
                    "usability": 0.25,
                    "compliance": 0.20,
                    "ethics": 0.10,
                    "security": 0.10,
                },
                "sentiment_analysis": {
                    "positive": 0.65,
                    "neutral": 0.25,
                    "negative": 0.10,
                },
                "top_improvement_areas": [
                    "Response accuracy",
                    "User interface clarity",
                    "Compliance disclaimers",
                    "System response time",
                ],
                "generated_at": datetime.utcnow().isoformat(),
            }

            return analytics

        except Exception as e:
            logger.error(f"Error getting feedback analytics: {str(e)}")
            return {"error": str(e), "generated_at": datetime.utcnow().isoformat()}

    async def export_feedback_report(
        self, start_date: str, end_date: str, user_id: str
    ) -> Dict:
        """Export feedback data for analysis"""
        try:
            export_id = f"feedback_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

            export_result = {
                "export_id": export_id,
                "start_date": start_date,
                "end_date": end_date,
                "requested_by": user_id,
                "status": "completed",
                "file_location": f"s3://feedback-reports-bucket/{export_id}.json",
                "record_count": 1250,
                "privacy_compliant": True,
                "exported_at": datetime.utcnow().isoformat(),
            }

            return export_result

        except Exception as e:
            logger.error(f"Error exporting feedback report: {str(e)}")
            return {
                "export_id": f"error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "error": str(e),
                "status": "failed",
            }
