import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shoop-stripe",
        version="0.1.2",
        description="Stripe Checkout integration for Shoop",
        packages=["shoop_stripe"],
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_stripe=shoop_stripe"}
    )
