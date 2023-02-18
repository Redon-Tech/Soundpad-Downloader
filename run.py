from downloader import create_app

app = create_app()


def main():
    app.run(host="10.0.0.159", debug=True)


if __name__ == "__main__":
    main()
