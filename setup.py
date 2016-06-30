import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shoop-stripe",
        version="0.2.0",
        description="Stripe Checkout integration for Shoop",
        packages=["shoop_stripe"],
        include_package_data=True,
        install_requires=["shoop>=4.0,<5.0"],
        entry_points={"shoop.addon": "shoop_stripe=shoop_stripe"}
    )
