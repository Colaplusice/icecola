from flask import Response, abort, jsonify, request
from flask.views import MethodView
from playhouse.shortcuts import model_to_dict


class ModelViewSet(MethodView):
    model_class = None

    def get(self, pk):
        query = self.model_class.select()
        if pk is not None:
            query = query.where(self.model_class.id == pk).first()
            if query is None:
                abort(status=404)
            return jsonify(model_to_dict(query, recurse=False))
        return jsonify([model_to_dict(q, recurse=False) for q in query])

    def post(self):
        data = request.json
        if not data:
            abort(400)
        model_instance = self.model_class.create(**data)
        res = jsonify(model_to_dict(model_instance, recurse=False)), 201
        return res

    def put(self, pk):
        updated = (
            self.model_class.update(**request.json)
            .where(self.model_class.id == pk)
            .execute()
        )
        return Response(status=204 if updated else 200)

    def delete(self, pk):
        self.model_class.delete_by_id(pk)
        return Response(status=204)
