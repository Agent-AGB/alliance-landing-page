@app.route("/new-lead", methods=["POST"])
def new_lead():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            data = request.form.to_dict()
        if not data:
            data = {}
        print("New lead received: " + str(data))
        handle_new_lead(data)
    except Exception as e:
        print("Error: " + str(e))
    return jsonify({"status": "success"}), 200