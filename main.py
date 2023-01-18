from flask import Flask, request, jsonify, make_response, send_file
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)


class AbstractCipher(Resource):

    def implement_abs_cipher(self, string):
        order = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        reverse = 'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA'
        dictChars = dict(zip(order, reverse))
        output = []
        for item in string:

            if item == ' ':
                output.append('@')
            elif item not in dictChars.keys():
                output.append(item)
            else:
                output.append(dictChars[item])

        output = "".join(output)
        output2 = output.replace('@', ' ')
        return output2

    def post(self):
        if 'file' not in request.files:
            return make_response(jsonify({"error": True, "message": "File not found in the request"}), 403)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            with open(filename, 'r') as f:
                file_content = f.read()
            encrypted_data = self.implement_abs_cipher(file_content)
            with open(filename, 'w') as f:
                f.write(encrypted_data)
            return send_file(filename)


api.add_resource(AbstractCipher, '/abstract_cipher', endpoint='abstract_cipher')

if __name__ == '__main__':
    app.run()
