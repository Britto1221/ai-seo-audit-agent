from seoextract import SEOExtract

result = SEOExtract.audit("https://www.shopify.com")
print(result.model_dump_json(indent=2))