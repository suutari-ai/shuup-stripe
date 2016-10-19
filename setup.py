import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shuup-stripe",
        version="0.4.1",
        description="Stripe Checkout integration for Shuup",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=["shuup>=0.4"],
        entry_points={"shuup.addon": "shuup_stripe=shuup_stripe"}
    )
