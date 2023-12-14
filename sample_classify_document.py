# coding: utf-8

"""
FILE: sample_classify_document.py

DESCRIPTION:
    This sample demonstrates how to classify a document using a trained document classifier.
    To learn how to build your custom classifier, see sample_build_classifier.py.

USAGE:
    python sample_classify_document.py
"""

import os
import sys
from azure.core.exceptions import HttpResponseError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, DocumentModelAdministrationClient, ClassifierDocumentTypeDetails, BlobSource

# Print Python Path and Location of Azure module for debugging
print("Python Path:", sys.path)
print("Location of azure module:", sys.modules.get('azure'))

def classify_document(file_stream, classifier_id="invoice-or-resume"):
    endpoint = "https://clee-ai-docint-01.cognitiveservices.azure.com/"
    key = "7575f723a3f64974a4c76a347540ee21"

    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    # Use the file stream directly
    poller = document_analysis_client.begin_classify_document(classifier_id, document=file_stream)
    result = poller.result()

    classified_docs = []
    for doc in result.documents:
        classified_doc = {
            "type": doc.doc_type or 'N/A',
            "confidence": doc.confidence,
            "pages": [region.page_number for region in doc.bounding_regions]
        }
        classified_docs.append(classified_doc)

    return classified_docs

if __name__ == "__main__":
    try:
        classifier_id = "invoice-or-resume"

        # Path to your sample document
        path_to_sample_documents = "C:/Users/chris/OneDrive/Documents/docint/resumes/test resume Vienna-Modern-Resume-Template.pdf"

        # Use the Blob SAS URL directly (Not recommended for production code)
        blob_container_sas_url = "https://cleeaidocintsa.blob.core.windows.net/customeraddress?sp=racwdli&st=2023-12-14T20:48:34Z&se=2023-12-15T04:48:34Z&spr=https&sv=2022-11-02&sr=c&sig=JWo7CNX4Vin85wsxd%2B1ER%2BpB5%2BHsEYb7Fx01LyrLrL0%3D"

        if blob_container_sas_url:
            endpoint = "https://clee-ai-docint-01.cognitiveservices.azure.com/"
            key = "7575f723a3f64974a4c76a347540ee21"

            document_model_admin_client = DocumentModelAdministrationClient(endpoint=endpoint, credential=AzureKeyCredential(key))

            poller = document_model_admin_client.begin_build_document_classifier(
                doc_types={
                    "Invoice": ClassifierDocumentTypeDetails(
                        source=BlobSource(container_url=blob_container_sas_url, prefix="")
                    ),
                    "Resume": ClassifierDocumentTypeDetails(
                        source=BlobSource(container_url=blob_container_sas_url, prefix="")
                    ),
                }
            )

            classifier = poller.result()
            classifier_id = classifier.classifier_id

        classify_document(classifier_id, path_to_sample_documents)

    except HttpResponseError as error:
        print("For more information about troubleshooting errors, see the following guide: https://aka.ms/azsdk/python/formrecognizer/troubleshooting")
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            raise
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        raise
