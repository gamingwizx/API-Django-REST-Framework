from rest_framework.throttling import UserRateThrottle

class AddReviewThrottle(UserRateThrottle):
    scope = 'add_review'

class UpdateReviewThrottle(UserRateThrottle):
    scope = "update_review"