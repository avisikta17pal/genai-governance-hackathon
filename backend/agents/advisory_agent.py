import logging
import boto3
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class AdvisoryAgent:
    """
    Advisory Agent: Provides user-friendly guidance on governance decisions,
    compliant alternatives, and regulatory requirements. Answers questions about appropriate AI usage.
    """

    def __init__(self):
        self.bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Advisory knowledge base
        self.advisory_knowledge = {
            "gdpr_guidance": {
                "personal_data": {
                    "description": "Personal data includes any information that can identify an individual",
                    "examples": [
                        "name",
                        "email",
                        "phone number",
                        "IP address",
                        "cookies",
                    ],
                    "requirements": [
                        "Obtain explicit consent before processing",
                        "Implement data minimization",
                        "Provide right to be forgotten",
                        "Ensure data portability",
                    ],
                    "alternatives": [
                        "Use anonymized data when possible",
                        "Implement pseudonymization",
                        "Limit data collection to essential fields",
                    ],
                },
                "data_processing": {
                    "description": "Any operation performed on personal data",
                    "requirements": [
                        "Have a legal basis for processing",
                        "Document processing activities",
                        "Implement appropriate security measures",
                        "Conduct data protection impact assessments",
                    ],
                },
            },
            "hipaa_guidance": {
                "phi_protection": {
                    "description": "Protected Health Information must be safeguarded",
                    "examples": [
                        "medical records",
                        "diagnosis",
                        "treatment plans",
                        "billing information",
                    ],
                    "requirements": [
                        "Implement access controls",
                        "Use encryption for data at rest and in transit",
                        "Maintain audit logs",
                        "Train staff on HIPAA compliance",
                    ],
                    "alternatives": [
                        "Use de-identified data when possible",
                        "Implement role-based access controls",
                        "Use secure communication channels",
                    ],
                }
            },
            "ethical_ai_guidance": {
                "bias_prevention": {
                    "description": "Ensure AI systems are fair and unbiased",
                    "requirements": [
                        "Use diverse training data",
                        "Regularly test for bias",
                        "Implement fairness metrics",
                        "Provide explanations for decisions",
                    ],
                    "alternatives": [
                        "Use balanced datasets",
                        "Implement bias detection tools",
                        "Regular model retraining",
                    ],
                },
                "transparency": {
                    "description": "AI systems should be explainable and transparent",
                    "requirements": [
                        "Document model decisions",
                        "Provide clear explanations",
                        "Maintain audit trails",
                        "Enable human oversight",
                    ],
                },
            },
            "security_guidance": {
                "data_protection": {
                    "description": "Protect sensitive data from unauthorized access",
                    "requirements": [
                        "Implement encryption",
                        "Use secure authentication",
                        "Regular security audits",
                        "Incident response plan",
                    ],
                    "alternatives": [
                        "Use multi-factor authentication",
                        "Implement least privilege access",
                        "Regular penetration testing",
                    ],
                }
            },
        }

        # Common compliance scenarios
        self.compliance_scenarios = {
            "medical_advice": {
                "risk_level": "high",
                "guidance": "Medical advice should not be provided by AI systems without proper disclaimers and human oversight",
                "alternatives": [
                    "Provide general health information with disclaimers",
                    "Direct users to consult healthcare professionals",
                    "Use only for educational purposes",
                ],
                "required_disclaimers": [
                    "This is not medical advice",
                    "Consult a healthcare provider",
                    "For informational purposes only",
                ],
            },
            "financial_advice": {
                "risk_level": "high",
                "guidance": "Financial advice requires proper licensing and compliance with financial regulations",
                "alternatives": [
                    "Provide general financial education",
                    "Use historical data for analysis only",
                    "Direct to licensed financial advisors",
                ],
                "required_disclaimers": [
                    "This is not financial advice",
                    "Past performance does not guarantee future results",
                    "Consult a financial advisor",
                ],
            },
            "legal_advice": {
                "risk_level": "high",
                "guidance": "Legal advice should only be provided by licensed attorneys",
                "alternatives": [
                    "Provide general legal information",
                    "Direct to legal resources",
                    "Use for educational purposes only",
                ],
                "required_disclaimers": [
                    "This is not legal advice",
                    "Consult an attorney",
                    "For informational purposes only",
                ],
            },
        }

    async def provide_guidance(
        self, prompt: str, response: str, risk_assessment: Dict, audit_result: Dict
    ) -> Dict:
        """
        Provide guidance based on the prompt, response, and governance results
        """
        try:
            logger.info("Providing advisory guidance")

            # Step 1: Analyze the request context
            context_analysis = await self._analyze_context(prompt, response)

            # Step 2: Identify applicable guidance
            applicable_guidance = await self._identify_applicable_guidance(
                context_analysis
            )

            # Step 3: Generate recommendations
            recommendations = await self._generate_recommendations(
                context_analysis, applicable_guidance
            )

            # Step 4: Provide educational content
            educational_content = await self._provide_educational_content(
                applicable_guidance
            )

            result = {
                "guidance_type": context_analysis["guidance_type"],
                "risk_level": risk_assessment.get("risk_level", "unknown"),
                "recommendations": recommendations,
                "educational_content": educational_content,
                "compliance_requirements": applicable_guidance.get(
                    "compliance_requirements", []
                ),
                "alternatives": applicable_guidance.get("alternatives", []),
                "required_disclaimers": applicable_guidance.get(
                    "required_disclaimers", []
                ),
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": 0.9,
            }

            logger.info("Advisory guidance provided successfully")
            return result

        except Exception as e:
            logger.error(f"Error providing guidance: {str(e)}")
            return {
                "guidance_type": "general",
                "risk_level": "unknown",
                "recommendations": [
                    "Review the request and consult with compliance team"
                ],
                "educational_content": {},
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _analyze_context(self, prompt: str, response: str) -> Dict:
        """Analyze the context of the request to determine guidance type"""
        prompt_lower = prompt.lower()
        response_lower = response.lower()

        context_analysis = {
            "guidance_type": "general",
            "domains": [],
            "risk_indicators": [],
            "compliance_areas": [],
        }

        # Check for medical content
        medical_keywords = [
            "medical",
            "health",
            "diagnosis",
            "treatment",
            "symptoms",
            "medicine",
        ]
        if any(keyword in prompt_lower for keyword in medical_keywords):
            context_analysis["domains"].append("medical")
            context_analysis["guidance_type"] = "medical_advice"
            context_analysis["compliance_areas"].append("hipaa")

        # Check for financial content
        financial_keywords = [
            "investment",
            "financial",
            "money",
            "trading",
            "stock",
            "portfolio",
        ]
        if any(keyword in prompt_lower for keyword in financial_keywords):
            context_analysis["domains"].append("financial")
            context_analysis["guidance_type"] = "financial_advice"
            context_analysis["compliance_areas"].append("sox")

        # Check for legal content
        legal_keywords = [
            "legal",
            "law",
            "contract",
            "liability",
            "rights",
            "legal advice",
        ]
        if any(keyword in prompt_lower for keyword in legal_keywords):
            context_analysis["domains"].append("legal")
            context_analysis["guidance_type"] = "legal_advice"

        # Check for personal data
        personal_data_keywords = [
            "personal",
            "private",
            "email",
            "phone",
            "address",
            "ssn",
        ]
        if any(keyword in prompt_lower for keyword in personal_data_keywords):
            context_analysis["compliance_areas"].append("gdpr")

        # Check for bias indicators
        bias_keywords = ["bias", "discrimination", "stereotype", "prejudice"]
        if any(
            keyword in prompt_lower or keyword in response_lower
            for keyword in bias_keywords
        ):
            context_analysis["risk_indicators"].append("potential_bias")

        return context_analysis

    async def _identify_applicable_guidance(self, context_analysis: Dict) -> Dict:
        """Identify applicable guidance based on context analysis"""
        applicable_guidance = {
            "compliance_requirements": [],
            "alternatives": [],
            "required_disclaimers": [],
            "educational_content": {},
        }

        # Add guidance based on domains
        for domain in context_analysis["domains"]:
            if domain in self.compliance_scenarios:
                scenario = self.compliance_scenarios[domain]
                applicable_guidance["compliance_requirements"].extend(
                    scenario.get("guidance", "").split(". ")
                )
                applicable_guidance["alternatives"].extend(
                    scenario.get("alternatives", [])
                )
                applicable_guidance["required_disclaimers"].extend(
                    scenario.get("required_disclaimers", [])
                )

        # Add guidance based on compliance areas
        for area in context_analysis["compliance_areas"]:
            if area in self.advisory_knowledge:
                area_guidance = self.advisory_knowledge[area]
                for key, guidance in area_guidance.items():
                    applicable_guidance["compliance_requirements"].extend(
                        guidance.get("requirements", [])
                    )
                    applicable_guidance["alternatives"].extend(
                        guidance.get("alternatives", [])
                    )
                    applicable_guidance["educational_content"][key] = guidance

        return applicable_guidance

    async def _generate_recommendations(
        self, context_analysis: Dict, applicable_guidance: Dict
    ) -> List[str]:
        """Generate specific recommendations based on context and guidance"""
        recommendations = []

        # General recommendations
        recommendations.append(
            "Always review AI-generated content for accuracy and compliance"
        )
        recommendations.append("Implement appropriate disclaimers for sensitive topics")
        recommendations.append("Maintain audit trails for all AI interactions")

        # Domain-specific recommendations
        if "medical" in context_analysis["domains"]:
            recommendations.append(
                "Add medical disclaimers to all health-related content"
            )
            recommendations.append("Ensure HIPAA compliance for any patient data")
            recommendations.append(
                "Direct users to healthcare professionals for specific advice"
            )

        if "financial" in context_analysis["domains"]:
            recommendations.append(
                "Add financial disclaimers to all investment-related content"
            )
            recommendations.append("Ensure compliance with financial regulations")
            recommendations.append("Direct users to licensed financial advisors")

        if "legal" in context_analysis["domains"]:
            recommendations.append("Add legal disclaimers to all legal-related content")
            recommendations.append("Ensure compliance with legal regulations")
            recommendations.append("Direct users to licensed attorneys")

        # Risk-specific recommendations
        if "potential_bias" in context_analysis["risk_indicators"]:
            recommendations.append(
                "Review content for potential bias and discrimination"
            )
            recommendations.append("Implement bias detection and mitigation strategies")
            recommendations.append("Use diverse and representative training data")

        # Add alternatives from applicable guidance
        recommendations.extend(applicable_guidance.get("alternatives", []))

        return recommendations

    async def _provide_educational_content(self, applicable_guidance: Dict) -> Dict:
        """Provide educational content about compliance and best practices"""
        educational_content = {
            "compliance_frameworks": {},
            "best_practices": {},
            "resources": {},
        }

        # Add educational content from applicable guidance
        for key, content in applicable_guidance.get("educational_content", {}).items():
            educational_content["compliance_frameworks"][key] = {
                "description": content.get("description", ""),
                "requirements": content.get("requirements", []),
                "examples": content.get("examples", []),
            }

        # Add general best practices
        educational_content["best_practices"] = {
            "data_protection": [
                "Always encrypt sensitive data",
                "Implement access controls",
                "Regular security audits",
                "Train staff on compliance",
            ],
            "ai_governance": [
                "Monitor AI system performance",
                "Regular bias testing",
                "Maintain transparency",
                "Enable human oversight",
            ],
            "compliance_monitoring": [
                "Regular compliance audits",
                "Update policies as needed",
                "Track regulatory changes",
                "Maintain documentation",
            ],
        }

        # Add helpful resources
        educational_content["resources"] = {
            "gdpr": "https://gdpr.eu/",
            "hipaa": "https://www.hhs.gov/hipaa/index.html",
            "ai_ethics": "https://www.ieee.org/ethics",
            "data_protection": "https://www.iso.org/standard/54534.html",
        }

        return educational_content

    async def answer_question(self, question: str, user_context: Dict) -> Dict:
        """Answer user questions about governance and compliance"""
        try:
            question_lower = question.lower()

            # Simple keyword-based question answering
            if "gdpr" in question_lower or "data protection" in question_lower:
                return await self._answer_gdpr_question(question)
            elif "hipaa" in question_lower or "medical" in question_lower:
                return await self._answer_hipaa_question(question)
            elif "bias" in question_lower or "fairness" in question_lower:
                return await self._answer_ethics_question(question)
            elif "security" in question_lower or "encryption" in question_lower:
                return await self._answer_security_question(question)
            else:
                return await self._answer_general_question(question)

        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "answer": "I apologize, but I cannot provide specific advice on this topic. Please consult with your compliance team.",
                "confidence": 0.5,
                "sources": [],
            }

    async def _answer_gdpr_question(self, question: str) -> Dict:
        """Answer GDPR-related questions"""
        return {
            "answer": "GDPR requires organizations to protect personal data and respect individual privacy rights. Key requirements include obtaining consent, implementing data minimization, and providing data subject rights.",
            "confidence": 0.9,
            "sources": ["GDPR Article 5", "GDPR Article 6"],
            "related_topics": [
                "data minimization",
                "consent management",
                "data subject rights",
            ],
        }

    async def _answer_hipaa_question(self, question: str) -> Dict:
        """Answer HIPAA-related questions"""
        return {
            "answer": "HIPAA protects patient health information and requires covered entities to implement safeguards for PHI. This includes access controls, encryption, and audit trails.",
            "confidence": 0.9,
            "sources": ["HIPAA Privacy Rule", "HIPAA Security Rule"],
            "related_topics": ["PHI protection", "access controls", "audit trails"],
        }

    async def _answer_ethics_question(self, question: str) -> Dict:
        """Answer AI ethics questions"""
        return {
            "answer": "AI systems should be fair, transparent, and accountable. This includes preventing bias, ensuring explainability, and maintaining human oversight.",
            "confidence": 0.8,
            "sources": ["IEEE Ethics Guidelines", "AI Ethics Framework"],
            "related_topics": ["bias detection", "transparency", "accountability"],
        }

    async def _answer_security_question(self, question: str) -> Dict:
        """Answer security-related questions"""
        return {
            "answer": "AI systems require robust security measures including encryption, access controls, and regular security audits to protect sensitive data and prevent unauthorized access.",
            "confidence": 0.8,
            "sources": ["ISO 27001", "NIST Cybersecurity Framework"],
            "related_topics": ["encryption", "access controls", "security audits"],
        }

    async def _answer_general_question(self, question: str) -> Dict:
        """Answer general governance questions"""
        return {
            "answer": "AI governance involves implementing policies and procedures to ensure responsible AI use, compliance with regulations, and protection of user rights.",
            "confidence": 0.7,
            "sources": ["AI Governance Framework"],
            "related_topics": ["compliance", "risk management", "audit trails"],
        }
