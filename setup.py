import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shuup-stripe",
        version="0.2.0",
        description="Stripe Checkout integration for Shuup",
        packages=["shuup_stripe"],
        include_package_data=True,
        install_requires=["shuup>=0.4"],
        entry_points={"shuup.addon": "shuup_stripe=shuup_stripe"}
    )
