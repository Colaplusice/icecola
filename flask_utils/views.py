def register_api(app, view, endpoint, url, pk="pk", pk_type="int"):
    """
    register_api(UserAPI, 'user_api', '/users/', pk='user_id')
    /users/ list user  post
    /users/1 get delete put
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=["GET"])
    app.add_url_rule(url, view_func=view_func, methods=["POST"])
    app.add_url_rule(
        "%s<%s:%s>" % (url, pk_type, pk),
        view_func=view_func,
        methods=["GET", "PUT", "DELETE"],
    )
