from django.db.models import Count

def update_user_reputation(user):
    upvotes = user.tip_set.aggregate(total_upvotes=Count('upvote'))['total_upvotes']
    downvotes = user.tip_set.aggregate(total_downvotes=Count('downvote'))['total_downvotes']
    user.reputation = upvotes * 5 - downvotes * 2
    
    user.can_downvote_by_reputation = user.reputation >= 15
    user.can_delete_by_reputation = user.reputation >= 30
    
    user.save(update_fields=['reputation', 'can_downvote_by_reputation', 'can_delete_by_reputation'])

def toggle_vote(tip, user, vote_type):
    if vote_type not in ['upvote', 'downvote']:
        raise ValueError("vote_type must be either 'upvote' or 'downvote'")
    
    if vote_type == 'downvote' and not (user.can_downvote() or tip.author == user):
        return False
    
    opposite_type = 'downvote' if vote_type == 'upvote' else 'upvote'
    vote_manager = getattr(tip, vote_type)
    opposite_manager = getattr(tip, opposite_type)
    
    if user in vote_manager.all():
        vote_manager.remove(user)
    else:
        opposite_manager.remove(user)
        vote_manager.add(user)
    
    update_user_reputation(tip.author)
    return True

