from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.document_indexing.models import (
    IndexInstanceNode, IndexTemplate
)
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_TEMPLATE_LABEL
from mayan.apps.testing.tests.base import BaseTestCase

from .literals import (
    TEST_TAG_INDEX_HAS_TAG, TEST_TAG_INDEX_NO_TAG,
    TEST_TAG_INDEX_NODE_TEMPLATE
)
from .mixins import TagTestMixin


class TagSignalIndexingTestCase(DocumentTestMixin, TagTestMixin, BaseTestCase):
    auto_upload_test_document = False

    def test_tag_indexing(self):
        self._create_test_tag()
        self.test_index_template = IndexTemplate.objects.create(
            label=TEST_INDEX_TEMPLATE_LABEL
        )
        self.test_index_template.document_types.add(self.test_document_type)

        root = self.test_index_template.template_root
        self.test_index_template.node_templates.create(
            parent=root, expression=TEST_TAG_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self._upload_test_document()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )

        self.test_tag.documents.add(self.test_document)

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_HAS_TAG
            ).documents.all()
        )

        self.test_tag.delete()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )
