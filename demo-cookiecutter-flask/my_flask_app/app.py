# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template

from my_flask_app import commands, public, user
from my_flask_app.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)


def create_app(config_object="my_flask_app.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    import os
    from functools import partial
    import sentry_sdk

    environment = "uk-memory-leak"

    def sentry_sampler(sampling_context, sample_rate=0):
        return 1
        # if sampling_context["parent_sampled"]:
        #     return 1

        # return sample_rate

    sentry_sdk.init(
        dsn="https://3718e65d184c45f385813778e1857bc1@o447951.ingest.sentry.io/6604845",
        environment=environment,
        debug=False,
        sample_rate=float(os.getenv("SENTRY_SAMPLE_RATE", 1.0)),
        attach_stacktrace=False,
        send_default_pii=False,
        request_bodies="never",
        enable_tracing=True,
        traces_sampler=partial(
            sentry_sampler, sample_rate=float(os.getenv("SENTRY_SAMPLE_RATE", 0))
        ),
    )

    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
