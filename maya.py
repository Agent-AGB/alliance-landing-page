if __name__ == "__main__":
    print("Maya AI Sales Assistant is starting!")
    print("------------------------------------------------------")
    test_maya()
    print("------------------------------------------------------")
    print("Starting webhook server...")
    port = int(os.environ.get("PORT", 8080))
    print("Running on port: " + str(port))
    app.run(host="0.0.0.0", port=port, debug=False)