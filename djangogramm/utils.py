from django.contrib.auth.decorators import user_passes_test

confirm_email_required = user_passes_test(lambda u: u.is_email_confirmed,
                                          login_url='email_not_confirmed')