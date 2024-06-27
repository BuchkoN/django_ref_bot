from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserFunnelText(IntegerChoices):
    first = 1, _(
        '"How to Gain Clients’ Trust? 💰"\n'
        'Build a personal brand by creating an illusion of success. '
        'Post photos from luxurious places, share stories of your "achievements" and '
        'always speak about yourself in superlatives.'
    )
    second = 2, _(
        '"The Art of Persuasive Copywriting 📝"\n'
        'Use catchy headlines and emotional appeals. Start with a problem, offer a solution, '
        'and show how your product has changed clients’ lives. '
        'Always add testimonials (even if they’re fictional).'
    )
    third = 3, _(
        '"Effective Social Media Strategies 📱"\n'
        'Post content regularly, engage with followers, run contests and giveaways. '
        'The more activity, the higher the trust in you and your product.'
    )
    fourth = 4, _(
        '"How to Create an Irresistible Offer? 🎁"\n'
        'Come up with a unique selling proposition (USP). Create limited-time offers and discounts, '
        'add bonuses for purchases, creating a sense of urgency and value for the client.'
    )
    fifth = 5, _(
        '"Automating the Sales Process 🚀"\n'
        'Set up sales funnels and email marketing. '
        'Use chatbots to interact with clients and sell your products. '
        'This will help you save time and increase profits without extra effort.'
    )

    @classmethod
    def get_next_funnel_label(cls, funnel_stage: str):
        stage = getattr(cls, funnel_stage).value
        if stage == cls.fifth.value:
            return None
        return cls.names[stage]

    @classmethod
    def get_prev_funnel_label(cls, funnel_stage: str):
        stage = getattr(cls, funnel_stage).value
        if stage == cls.first.value:
            return None
        return cls.names[stage - 2]


class BotMessagesText:
    SELECT_LANG = _('Please select a language')