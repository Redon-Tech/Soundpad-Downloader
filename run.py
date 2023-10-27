from downloader import create_app

app = create_app()


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
