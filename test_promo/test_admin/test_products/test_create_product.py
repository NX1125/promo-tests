class TestIncompleteFields:
    """
    Required fields for a product:
    - name
    - supplier
    - at least one variant
    - at least one decoration method per variant
    - a primary price table
    - at least one non-zero quantity per price table
    """

    def test_without_supplier(self):
        pass

    def test_without_variant(self):
        pass

    def test_without_decoration_method(self):
        pass

    def test_without_price_table(self):
        pass

    def test_without_quantity(self):
        pass

    def test_without_name(self):
        pass


def test_without_slug(admin_browser):
    """
    The slug should be created when saved.
    """
    pass
