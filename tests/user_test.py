from . import util
from okcupyd import User
from okcupyd.profile import Profile


@util.use_cassette('user_no_picture')
def test_handle_no_pictures():
    username = User().profile.username
    assert username is not None


@util.use_cassette('user_get_threads')
def test_get_inbox():
    user = User()
    assert len(user.inbox.items) == 1

    for message_thread in user.inbox:
        for message in message_thread.messages:
            assert hasattr(message, 'sender')


@util.use_cassette('access_profile_from_message_thread')
def test_message_thread_to_profile():
    profile = User().inbox[0].correspondent_profile
    assert profile.age
    assert profile.age > 18
    assert isinstance(profile.rating, int)


@util.use_cassette('user_count')
def test_user_search_count():
    assert len(User().search(count=1)) == 1


@util.use_cassette('test_user_essays')
def test_user_essays():
    user = User()
    first_essay = 'an essay'
    user.profile.essays.self_summary = first_essay
    assert user.profile.essays.self_summary == first_essay

    second_essay = 'next_essay'
    user.profile.essays.self_summary = second_essay

    assert user.profile.essays.self_summary == second_essay


@util.use_cassette('test_user_essays_refresh')
def test_user_essay_refresh():
    # Test Refresh Function
    user = User()
    user2 = User(user._session)
    user.message_me_if = 'other stuff'

    user2.profile.essays.refresh()
    assert user.profile.essays.message_me_if == user2.profile.essays.message_me_if


@util.use_cassette('visitors_test')
def test_visitors():
    user = User()
    assert isinstance(user.visitors[0], Profile)


@util.use_cassette('profile_titles')
def test_profile_titles():
    user = User()
    for essay_name in user.profile.essays.essay_names:
        setattr(user.profile.essays, essay_name, 'updated')

    assert user.profile.essays.short_name_to_title == {
        'favorites': 'Favorite books, movies, shows, music, and food',
        'friday_night': 'On a typical Friday night I am',
        'good_at': u'I\u2019m really good at',
        'message_me_if': 'You should message me if',
        'my_life': u'What I\u2019m doing with my life',
        'people_first_notice': 'The first things people usually notice about me',
        'private_admission': u'The most private thing I\u2019m willing to admit',
        'self_summary': 'My self-summary',
        'six_things': 'The six things I could never do without',
        'think_about': 'I spend a lot of time thinking about'
    }
