# pyright: reportMissingImports=false
import logging
import jwt
import boto3
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import hashlib
import secrets
import uuid

logger = logging.getLogger(__name__)


class AuthService:
    """
    Authentication and Authorization Service for the GenAI Governance System
    Handles user authentication, authorization, and role-based access control
    """

    def __init__(self):
        self.dynamodb_client = boto3.client("dynamodb", region_name="us-east-1")
        self.cognito_client = boto3.client("cognito-idp", region_name="us-east-1")
        self.iam_client = boto3.client("iam", region_name="us-east-1")
        self.sts_client = boto3.client("sts", region_name="us-east-1")

        # JWT configuration
        self.jwt_secret = (
            "your-secret-key-here"  # In production, use environment variable
        )
        self.jwt_algorithm = "HS256"
        self.jwt_expiration = 3600  # 1 hour

        # User roles and permissions
        self.user_roles = {
            "admin": {
                "permissions": [
                    "read",
                    "write",
                    "delete",
                    "admin",
                    "audit",
                    "policy_management",
                ],
                "data_access": "all",
                "can_override_policies": True,
                "can_access_audit_logs": True,
                "can_manage_users": True,
                "can_update_policies": True,
            },
            "manager": {
                "permissions": ["read", "write", "audit"],
                "data_access": "department",
                "can_override_policies": False,
                "can_access_audit_logs": True,
                "can_manage_users": False,
                "can_update_policies": False,
            },
            "analyst": {
                "permissions": ["read", "analytics"],
                "data_access": "department",
                "can_override_policies": False,
                "can_access_audit_logs": True,
                "can_manage_users": False,
                "can_update_policies": False,
            },
            "user": {
                "permissions": ["read"],
                "data_access": "own",
                "can_override_policies": False,
                "can_access_audit_logs": False,
                "can_manage_users": False,
                "can_update_policies": False,
            },
            "guest": {
                "permissions": ["read"],
                "data_access": "public",
                "can_override_policies": False,
                "can_access_audit_logs": False,
                "can_manage_users": False,
                "can_update_policies": False,
            },
        }

        # Session management
        self.active_sessions = {}  # In production, use Redis or DynamoDB

        # Rate limiting
        self.rate_limits = {
            "login_attempts": 5,  # per 15 minutes
            "api_requests": 100,  # per hour
            "failed_auth": 3,  # per 15 minutes
        }

    async def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify JWT token and return user information
        """
        try:
            # Decode JWT token
            payload = jwt.decode(
                token, self.jwt_secret, algorithms=[self.jwt_algorithm]
            )

            # Check if token is expired
            if datetime.utcnow().timestamp() > payload.get("exp", 0):
                logger.warning("Token expired")
                return None

            # Get user information from payload
            user_id = payload.get("user_id")
            user_role = payload.get("role", "user")

            # Verify user exists and is active
            user_info = await self._get_user_info(user_id)
            if not user_info or not user_info.get("active", False):
                logger.warning(f"User {user_id} not found or inactive")
                return None

            # Check if session is still valid
            session_id = payload.get("session_id")
            if not await self._verify_session(session_id, user_id):
                logger.warning(f"Invalid session {session_id} for user {user_id}")
                return None

            return {
                "user_id": user_id,
                "role": user_role,
                "permissions": self.user_roles.get(user_role, {}).get(
                    "permissions", []
                ),
                "session_id": session_id,
                "expires_at": payload.get("exp"),
            }

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None

    async def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user with username and password
        """
        try:
            # In production, this would use AWS Cognito or similar
            # For demo purposes, we'll simulate authentication

            # Simulate user lookup
            user_info = await self._get_user_by_username(username)
            if not user_info:
                logger.warning(f"User {username} not found")
                return None

            # Verify password (in production, use proper password hashing)
            if not await self._verify_password(
                password, user_info.get("password_hash", "")
            ):
                logger.warning(f"Invalid password for user {username}")
                await self._record_failed_login(username)
                return None

            # Generate session
            session_id = await self._create_session(user_info["user_id"])

            # Generate JWT token
            token = await self._generate_token(user_info, session_id)

            return {
                "user_id": user_info["user_id"],
                "username": username,
                "role": user_info.get("role", "user"),
                "token": token,
                "session_id": session_id,
                "expires_at": datetime.utcnow()
                + timedelta(seconds=self.jwt_expiration),
            }

        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return None

    async def is_admin(self, user_id: str) -> bool:
        """Check if user has admin privileges"""
        try:
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return False

            return user_info.get("role") == "admin"

        except Exception as e:
            logger.error(f"Error checking admin status: {str(e)}")
            return False

    async def can_access_logs(self, user_id: str, session_id: str) -> bool:
        """Check if user can access audit logs"""
        try:
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return False

            role = user_info.get("role", "user")
            role_config = self.user_roles.get(role, {})

            return role_config.get("can_access_audit_logs", False)

        except Exception as e:
            logger.error(f"Error checking log access: {str(e)}")
            return False

    async def can_access_analytics(self, user_id: str) -> bool:
        """Check if user can access analytics"""
        try:
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return False

            role = user_info.get("role", "user")
            permissions = self.user_roles.get(role, {}).get("permissions", [])

            return "analytics" in permissions or "admin" in permissions

        except Exception as e:
            logger.error(f"Error checking analytics access: {str(e)}")
            return False

    async def _get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information from database"""
        try:
            # In production, this would query DynamoDB
            # For demo, we'll return simulated user data

            # Simulate user database
            users = {
                "admin_001": {
                    "user_id": "admin_001",
                    "username": "admin",
                    "role": "admin",
                    "active": True,
                    "email": "admin@company.com",
                    "department": "IT",
                },
                "manager_001": {
                    "user_id": "manager_001",
                    "username": "manager",
                    "role": "manager",
                    "active": True,
                    "email": "manager@company.com",
                    "department": "Operations",
                },
                "analyst_001": {
                    "user_id": "analyst_001",
                    "username": "analyst",
                    "role": "analyst",
                    "active": True,
                    "email": "analyst@company.com",
                    "department": "Analytics",
                },
                "user_001": {
                    "user_id": "user_001",
                    "username": "user",
                    "role": "user",
                    "active": True,
                    "email": "user@company.com",
                    "department": "General",
                },
            }

            return users.get(user_id)

        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            return None

    async def _get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            # Simulate username lookup
            username_mapping = {
                "admin": "admin_001",
                "manager": "manager_001",
                "analyst": "analyst_001",
                "user": "user_001",
            }

            user_id = username_mapping.get(username)
            if user_id:
                return await self._get_user_info(user_id)

            return None

        except Exception as e:
            logger.error(f"Error getting user by username: {str(e)}")
            return None

    async def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            # In production, use proper password hashing (bcrypt, etc.)
            # For demo, we'll use simple hash comparison
            input_hash = hashlib.sha256(password.encode()).hexdigest()
            return input_hash == password_hash

        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False

    async def _create_session(self, user_id: str) -> Optional[str]:
        """Create a new user session"""
        try:
            session_id = f"session_{secrets.token_hex(16)}"

            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=8)).isoformat(),
                "active": True,
            }

            # Store session (in production, use DynamoDB or Redis)
            self.active_sessions[session_id] = session_data

            logger.info(f"Created session {session_id} for user {user_id}")
            return session_id

        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            return None

    async def _verify_session(self, session_id: str, user_id: str) -> bool:
        """Verify if session is valid"""
        try:
            if not session_id:
                return False

            session_data = self.active_sessions.get(session_id)
            if not session_data:
                return False

            # Check if session belongs to user
            if session_data.get("user_id") != user_id:
                return False

            # Check if session is active
            if not session_data.get("active", False):
                return False

            # Check if session is expired
            expires_at = datetime.fromisoformat(
                session_data.get("expires_at", "1970-01-01T00:00:00")
            )
            if datetime.utcnow() > expires_at:
                # Remove expired session
                self.active_sessions.pop(session_id, None)
                return False

            return True

        except Exception as e:
            logger.error(f"Error verifying session: {str(e)}")
            return False

    async def _generate_token(self, user_info: Dict, session_id: Optional[str]) -> Optional[str]:
        """Generate JWT token for user"""
        try:
            payload = {
                "user_id": user_info["user_id"],
                "username": user_info["username"],
                "role": user_info.get("role", "user"),
                "session_id": session_id,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(seconds=self.jwt_expiration),
            }

            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            return token

        except Exception as e:
            logger.error(f"Error generating token: {str(e)}")
            return None

    async def _record_failed_login(self, username: str) -> None:
        """Record failed login attempt for rate limiting"""
        try:
            # In production, this would store in DynamoDB
            # For demo, we'll just log it
            logger.warning(f"Failed login attempt for user: {username}")

        except Exception as e:
            logger.error(f"Error recording failed login: {str(e)}")

    async def logout(self, session_id: str) -> bool:
        """Logout user by invalidating session"""
        try:
            if session_id in self.active_sessions:
                self.active_sessions.pop(session_id)
                logger.info(f"Logged out session: {session_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return False

    async def get_user_permissions(self, user_id: str) -> List[str]:
        """Get user permissions"""
        try:
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return []

            role = user_info.get("role", "user")
            return self.user_roles.get(role, {}).get("permissions", [])

        except Exception as e:
            logger.error(f"Error getting user permissions: {str(e)}")
            return []

    async def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has specific permission"""
        try:
            permissions = await self.get_user_permissions(user_id)
            return permission in permissions

        except Exception as e:
            logger.error(f"Error checking permission: {str(e)}")
            return False

    async def verify_aws_iam_permissions(self, user_id: str, required_permissions: List[str]) -> Dict:
        """
        Verify AWS IAM permissions for the user
        """
        try:
            # Get user's AWS role/identity
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return {"authorized": False, "reason": "User not found"}

            # Check if user has AWS credentials/role
            aws_role = user_info.get("aws_role")
            if not aws_role:
                return {"authorized": False, "reason": "No AWS role configured"}

            # Verify permissions using AWS IAM
            try:
                # Get user's IAM policies
                policies = self.iam_client.list_attached_user_policies(UserName=user_id)
                
                # Check if user has required permissions
                authorized_permissions = []
                for permission in required_permissions:
                    if await self._check_iam_permission(user_id, permission):
                        authorized_permissions.append(permission)

                return {
                    "authorized": len(authorized_permissions) == len(required_permissions),
                    "authorized_permissions": authorized_permissions,
                    "missing_permissions": [p for p in required_permissions if p not in authorized_permissions],
                    "aws_role": aws_role,
                    "source": "aws_iam",
                }

            except Exception as e:
                logger.error(f"AWS IAM verification error: {str(e)}")
                return {
                    "authorized": False,
                    "reason": f"AWS IAM error: {str(e)}",
                    "source": "aws_iam_error",
                }

        except Exception as e:
            logger.error(f"Error verifying AWS IAM permissions: {str(e)}")
            return {"authorized": False, "reason": str(e)}

    async def _check_iam_permission(self, user_id: str, permission: str) -> bool:
        """
        Check if user has specific IAM permission
        """
        try:
            # Simulate IAM permission check
            # In production, you would use AWS IAM policy evaluation
            
            # Map permissions to IAM actions
            permission_mapping = {
                "read": ["s3:GetObject", "dynamodb:GetItem"],
                "write": ["s3:PutObject", "dynamodb:PutItem"],
                "delete": ["s3:DeleteObject", "dynamodb:DeleteItem"],
                "admin": ["*"],
                "audit": ["cloudtrail:LookupEvents", "logs:DescribeLogGroups"],
                "policy_management": ["iam:AttachUserPolicy", "iam:DetachUserPolicy"],
                "analytics": ["athena:StartQueryExecution", "quicksight:DescribeDashboard"],
            }

            required_actions = permission_mapping.get(permission, [])
            
            # For demo purposes, simulate permission check based on user role
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return False

            role = user_info.get("role", "user")
            
            # Admin has all permissions
            if role == "admin":
                return True
            
            # Check role-based permissions
            role_permissions = self.user_roles.get(role, {}).get("permissions", [])
            return permission in role_permissions

        except Exception as e:
            logger.error(f"Error checking IAM permission: {str(e)}")
            return False

    async def get_aws_credentials_info(self, user_id: str) -> Dict:
        """
        Get AWS credentials information for the user
        """
        try:
            # Get current AWS identity
            identity = self.sts_client.get_caller_identity()
            
            user_info = await self._get_user_info(user_id)
            if not user_info:
                return {"error": "User not found"}

            return {
                "user_id": user_id,
                "aws_account": identity.get("Account"),
                "aws_arn": identity.get("Arn"),
                "aws_user_id": identity.get("UserId"),
                "role": user_info.get("role", "user"),
                "permissions": self.user_roles.get(user_info.get("role", "user"), {}).get("permissions", []),
                "source": "aws_sts",
            }

        except Exception as e:
            logger.error(f"Error getting AWS credentials info: {str(e)}")
            return {"error": str(e)}
