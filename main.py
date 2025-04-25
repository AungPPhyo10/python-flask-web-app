from website import create_app      # import create_app from the website package

app = create_app()

if __name__ == '__main__':      # only run the app if the file is execute directly
    app.run(debug=True, port=5001) 