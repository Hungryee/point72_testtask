import requests


class Parser(object):

    def __init__(self) -> None:
        super().__init__()
        self.session = requests.session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'content-type': 'application/json',
            # this header is required for correct work
            'x-experience-name': 'major-appliances',
        }
        # here we can add new stores to parse
        self.stores = {
            # id as key
            2414: {
                'zip': 10022,
                'address': 'Manhattan 59th Street #6177, 980 3rd AveNew York, NY 10022'
            },
            589: {
                'zip': 75209,
                'address': 'Lemmon Ave #0589, 6110 Lemmon AveDallas, TX 75209'
            },
        }
        # here we can add new brands and/or categories
        self.filters = {
            'Appliances': {
                'subs':{
                    'Dishwasher': {
                        'LG Electronics': '5yc1vZc3poZ21j',
                        'Samsung': '5yc1vZc3poZa0f',
                    },
                    'Refrigerators': {
                        'Whirlpool': '5yc1vZc3piZ4l4',
                        'GE': '5yc1vZc3piZlo'
                    }
                },
                'experience':'major-appliances',
            },
            'Furniture-Bedroom-Furniture': {
                'subs':{
                    'Mattresses': {
                        'Sealy': '5yc1vZc7oeZf98'
                    }
                },
                'experience':'hd-home',
            }
        }

    def get_list_api_url(self):
        return f'https://www.homedepot.com/federation-gateway/graphql?opname=searchModel'

    def get_payload_list(self, store_id, store_zip, page_num=0, navparam=None):
        # 0-based indexing
        page_size = 24
        offset = page_num * page_size
        return {"operationName": "searchModel",
                "variables": {
                    "skipInstallServices": False,
                    "skipKPF": False,
                    "skipSpecificationGroup": False,
                    "skipSubscribeAndSave": False,
                    "storefilter": "ALL",
                    "channel": "DESKTOP",
                    "additionalSearchParams": {
                        "sponsored": True,
                        "mcvisId": "11265682665224872711953357262396737576",
                        "deliveryZip": f"{store_zip}"  # for safety assume delivery to same zipcode
                    },
                    "filter": {},
                    "navParam": f"{navparam}",
                    "orderBy": {"field": "TOP_SELLERS", "order": "ASC"},
                    "pageSize": page_size,
                    "startIndex": offset,
                    "storeId": f"{store_id}"
                },
                "query": "query searchModel($storeId: String, $zipCode: String, $skipInstallServices: Boolean = true, $startIndex: Int, $pageSize: Int, $orderBy: ProductSort, $filter: ProductFilter, $skipKPF: Boolean = false, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false, $keyword: String, $navParam: String, $storefilter: StoreFilter = ALL, $itemIds: [String], $channel: Channel = DESKTOP, $additionalSearchParams: AdditionalParams, $loyaltyMembershipInput: LoyaltyMembershipInput) {\n  searchModel(keyword: $keyword, navParam: $navParam, storefilter: $storefilter, storeId: $storeId, itemIds: $itemIds, channel: $channel, additionalSearchParams: $additionalSearchParams, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    metadata {\n      categoryID\n      analytics {\n        semanticTokens\n        dynamicLCA\n        __typename\n      }\n      canonicalUrl\n      searchRedirect\n      clearAllRefinementsURL\n      contentType\n      isStoreDisplay\n      productCount {\n        inStore\n        __typename\n      }\n      stores {\n        storeId\n        storeName\n        address {\n          postalCode\n          __typename\n        }\n        nearByStores {\n          storeId\n          storeName\n          distance\n          address {\n            postalCode\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    products(startIndex: $startIndex, pageSize: $pageSize, orderBy: $orderBy, filter: $filter) {\n      identifiers {\n        storeSkuNumber\n        canonicalUrl\n        brandName\n        itemId\n        productLabel\n        modelNumber\n        productType\n        parentId\n        isSuperSku\n        __typename\n      }\n      installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) {\n        scheduleAMeasure\n        gccCarpetDesignAndOrderEligible\n        __typename\n      }\n      itemId\n      dataSources\n      media {\n        images {\n          url\n          type\n          subType\n          sizes\n          __typename\n        }\n        __typename\n      }\n      pricing(storeId: $storeId) {\n        value\n        alternatePriceDisplay\n        alternate {\n          bulk {\n            pricePerUnit\n            thresholdQuantity\n            value\n            __typename\n          }\n          unit {\n            caseUnitOfMeasure\n            unitsOriginalPrice\n            unitsPerCase\n            value\n            __typename\n          }\n          __typename\n        }\n        original\n        mapAboveOriginalPrice\n        message\n        preferredPriceFlag\n        promotion {\n          type\n          description {\n            shortDesc\n            longDesc\n            __typename\n          }\n          dollarOff\n          percentageOff\n          savingsCenter\n          savingsCenterPromos\n          specialBuySavings\n          specialBuyDollarOff\n          specialBuyPercentageOff\n          dates {\n            start\n            end\n            __typename\n          }\n          __typename\n        }\n        specialBuy\n        unitOfMeasure\n        __typename\n      }\n      reviews {\n        ratingsReviews {\n          averageRating\n          totalReviews\n          __typename\n        }\n        __typename\n      }\n      availabilityType {\n        discontinued\n        type\n        __typename\n      }\n      badges(storeId: $storeId) {\n        name\n        __typename\n      }\n      details {\n        collection {\n          collectionId\n          name\n          url\n          __typename\n        }\n        __typename\n      }\n      favoriteDetail {\n        count\n        __typename\n      }\n      fulfillment(storeId: $storeId, zipCode: $zipCode) {\n        backordered\n        backorderedShipDate\n        bossExcludedShipStates\n        excludedShipStates\n        seasonStatusEligible\n        fulfillmentOptions {\n          type\n          fulfillable\n          services {\n            type\n            hasFreeShipping\n            freeDeliveryThreshold\n            locations {\n              curbsidePickupFlag\n              isBuyInStoreCheckNearBy\n              distance\n              inventory {\n                isOutOfStock\n                isInStock\n                isLimitedQuantity\n                isUnavailable\n                quantity\n                maxAllowedBopisQty\n                minAllowedBopisQty\n                __typename\n              }\n              isAnchor\n              locationId\n              storeName\n              state\n              type\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      info {\n        hasSubscription\n        isBuryProduct\n        isSponsored\n        isGenericProduct\n        isLiveGoodsProduct\n        sponsoredBeacon {\n          onClickBeacon\n          onViewBeacon\n          __typename\n        }\n        sponsoredMetadata {\n          campaignId\n          placementId\n          slotId\n          __typename\n        }\n        globalCustomConfigurator {\n          customExperience\n          __typename\n        }\n        returnable\n        hidePrice\n        productSubType {\n          name\n          link\n          __typename\n        }\n        categoryHierarchy\n        samplesAvailable\n        customerSignal {\n          previouslyPurchased\n          __typename\n        }\n        productDepartmentId\n        productDepartment\n        augmentedReality\n        ecoRebate\n        quantityLimit\n        sskMin\n        sskMax\n        unitOfMeasureCoverage\n        wasMaxPriceRange\n        wasMinPriceRange\n        swatches {\n          isSelected\n          itemId\n          label\n          swatchImgUrl\n          url\n          value\n          __typename\n        }\n        totalNumberOfOptions\n        paintBrand\n        dotComColorEligible\n        __typename\n      }\n      keyProductFeatures @skip(if: $skipKPF) {\n        keyProductFeaturesItems {\n          features {\n            name\n            refinementId\n            refinementUrl\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      specificationGroup @skip(if: $skipSpecificationGroup) {\n        specifications {\n          specName\n          specValue\n          __typename\n        }\n        specTitle\n        __typename\n      }\n      subscription @skip(if: $skipSubscribeAndSave) {\n        defaultfrequency\n        discountPercentage\n        subscriptionEnabled\n        __typename\n      }\n      sizeAndFitDetail {\n        attributeGroups {\n          attributes {\n            attributeName\n            dimensions\n            __typename\n          }\n          dimensionLabel\n          productType\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    id\n    searchReport {\n      totalProducts\n      didYouMean\n      correctedKeyword\n      keyword\n      pageSize\n      searchUrl\n      sortBy\n      sortOrder\n      startIndex\n      __typename\n    }\n    relatedResults {\n      universalSearch {\n        title\n        __typename\n      }\n      relatedServices {\n        label\n        __typename\n      }\n      visualNavs {\n        label\n        imageId\n        webUrl\n        categoryId\n        imageURL\n        __typename\n      }\n      visualNavContainsEvents\n      relatedKeywords {\n        keyword\n        __typename\n      }\n      __typename\n    }\n    taxonomy {\n      brandLinkUrl\n      breadCrumbs {\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionId\n        dimensionName\n        label\n        refinementKey\n        url\n        __typename\n      }\n      __typename\n    }\n    templates\n    partialTemplates\n    dimensions {\n      label\n      refinements {\n        refinementKey\n        label\n        recordCount\n        selected\n        imgUrl\n        url\n        nestedRefinements {\n          label\n          url\n          recordCount\n          refinementKey\n          __typename\n        }\n        __typename\n      }\n      collapse\n      dimensionId\n      isVisualNav\n      isVisualDimension\n      nestedRefinementsLimit\n      visualNavSequence\n      __typename\n    }\n    orangeGraph {\n      universalSearchArray {\n        pods {\n          title\n          description\n          imageUrl\n          link\n          __typename\n        }\n        info {\n          title\n          __typename\n        }\n        __typename\n      }\n      productTypes\n      __typename\n    }\n    appliedDimensions {\n      label\n      refinements {\n        label\n        refinementKey\n        url\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

    def generate_urls(self):
        for dep, values in self.filters.items():
            experience = values['experience']
            subs = values['subs']
            for sub, brands in subs.items():
                for brand, navparam in brands.items():
                    brand = brand.replace(' ', '-')
                    request_url = f'https://www.homedepot.com/b/{dep}-{sub}/{brand}/N-{navparam}'
                    metadata = {
                        'department': dep,
                        'subdepartment': sub,
                        'brand': brand,
                        'navparam': navparam,
                        'experience': experience
                    }
                    yield request_url, metadata

    def parse_list(self):
        flat_result = []

        for request_url, metadata in self.generate_urls():
            print('==================================================')
            self.session.headers['x-experience-name'] = metadata['experience']
            for store_id, store_vals in self.stores.items():
                print('--------------------------------------------------')
                store_zip = store_vals['zip']
                store_addr = store_vals['address']
                metadata['store_zip'] = store_zip
                metadata['store_address'] = store_addr

                for page_num in range(0, 100):
                    print(f'[PAGE {page_num}] Now querying {request_url} in store #{store_id}')
                    nav_param = request_url.split('/')[-1]

                    request = self.session.get(request_url)  # for cookies
                    request = self.session.post(self.get_list_api_url(),
                                                json=self.get_payload_list(store_id, store_zip, page_num, nav_param))
                    try:
                        request = request.json()
                        if len(request['data']['searchModel']['products']) == 0:
                            print('Empty page')
                            break
                    except:
                        break

                    for row in request['data']['searchModel']['products']:
                        item = self.parse_product(row)
                        item['metadata'] = metadata
                        flat_result.append(item)
        return flat_result

    def parse_product(self, row):
        item = {}
        try:
            item['model_label'] = row['identifiers']['productLabel']
        except Exception as e:
            item['model_label'] = None
        try:
            item['url'] = 'https://www.homedepot.com/' + row['identifiers']['canonicalUrl']
        except Exception as e:
            item['url'] = None
        try:
            item['producer'] = row['identifiers']['brandName']
        except Exception as e:
            item['producer'] = None
        try:
            item['model_number'] = row['identifiers']['modelNumber']
        except Exception as e:
            item['model_number'] = None

        try:
            item['price'] = row['pricing']['value']
        except Exception as e:
            item['price'] = None


        try:
            item['features'] = []
            for e in row['keyProductFeatures']['keyProductFeaturesItems'][0]['features']:
                item['features'].append({
                    'name': e['name'],
                    'value': e['value']
                })
        except Exception as e:
            item['features'] = None
        try:
            promotion = row['pricing']['promotion']
            if promotion['dollarOff'] != 0:
                item['promoted_price'] = item['price'] - promotion['dollarOff']
            else:
                item['promoted_price'] = None
        except Exception as e:
            print(e)
            item['promoted_price'] = None
        # print(dict(item))
        return item


if __name__ == '__main__':
    result = Parser().parse_list()
    print(result)
