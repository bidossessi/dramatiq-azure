# How to contribute

Thank you for wanting to give this project a hand. It's really appreciated.

This aproject is developped with `Python`.
To get your development  environment started, here are a few tips.

Have [poetry](https://python-poetry.org/docs/#installation) installed.

Fork, then clone the repo:

```shell
git clone git@github.com:your-username/dramatiq-azure.git
```

Set up your machine:

```
cd path/to/the/code
poetry install
```

Set-up pre-commit rules
```
poetry run pre-commit install
```
Make sure the tests pass:

```shell
poetry run pytest
```

Make your change. Add tests for your change. Make the tests pass.
Your tests should follow the [Arrange, Act and Assert](https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html) pattern as much as possible.

```
poetry run pytest
```


All green? You're ready to submit a [pull request](https://github.com/bidossessi/dramatiq-azure/compare).
Let us know:
- what the issue was (link to an existing issue?)
- a short description of how you solve it

And you're done!

As soon as possible, your changes will be reviewed for inclusion into the codebase if all goes well, with our thanks.

**Working on your first Pull Request?** You can learn how from this *free* series [How to Contribute to an Open Source Project on GitHub](https://kcd.im/pull-request)
