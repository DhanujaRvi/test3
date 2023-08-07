"""
Description: This file contains all the default values of Fields and Document Types 
             which are loaded when deployed
"""

fields_default = [
    #field_id = 1
    {
        "name"          : "vendor_name",
        "field_name"    : "Vendor Name",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "name_address", 
        "field_category": "Name Address Details" ,
        "type"          : "default"
    },
    #field_id = 2
    {
        "name"          : "vendor_address",
        "field_name"    : "Vendor Address",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "name_address", 
        "field_category": "Name Address Details" , 
        "type"          : "default"
    },
    #field_id = 3
    {
        "name"          : "customer_name",
        "field_name"    : "Customer Name",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "name_address",  
        "field_category": "Name Address Details" ,
        "type"          : "default"
    },
    #field_id = 4
    {
        "name"          : "customer_address",
        "field_name"    : "Customer Address",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "name_address",  
        "field_category": "Name Address Details" ,
        "type"          : "default"
    },
    #field_id = 5
    {
        "name"          : "invoice_number",
        "field_name"    : "Invoice Number",
        "descp"         : "",
        "dType"         : "Alphanumeric",
        "category"      : "invoice_details",  
        "field_category": "Invoice Details" ,
        "type"          : "default"
    },
    #field_id = 6
    {
        "name"          : "invoice_date",
        "field_name"    : "Invoice Date",
        "descp"         : "",
        "dType"         : "Date",
        "category"      : "invoice_details",  
        "field_category": "Invoice Details" ,
        "type"          : "default"
    },
    #field_id = 7
    {
        "name"          : "po_number",
        "field_name"    : "PO Number",
        "descp"         : "",
        "dType"         : "Alphanumeric",
        "category"      : "invoice_details",  
        "field_category": "Invoice Details" ,
        "type"          : "default"
    },
    #field_id = 8
    {
        "name"          : "total_amount",
        "field_name"    : "Total Amount",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 9
    {
        "name"          : "subtotal_amount",
        "field_name"    : "Subtotal Amount",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 10
    {
        "name"          : "tax_amount",
        "field_name"    : "Tax Amount",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 11
    {
        "name"          : "sgst",
        "field_name"    : "SGST",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details", 
        "field_category": "Amount Details" , 
        "type"          : "default"
    },
    #field_id = 12
    {
        "name"          : "cgst",
        "field_name"    : "CGST",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 13
    {
        "name"          : "igst",
        "field_name"    : "IGST",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 14
    {
        "name"          : "vendor_gstin",
        "field_name"    : "Vendor GSTIN",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 15
    {
        "name"          : "customer_gstin",
        "field_name"    : "Customer GSTIN",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 16
    {
        "name"          : "description",
        "field_name"    : "Description",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 17
    {
        "name"          : "quantity",
        "field_name"    : "Quantity",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 18
    {
        "name"          : "unitprice",
        "field_name"    : "Unit Price",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 19
    {
        "name"          : "amount",
        "field_name"    : "Amount",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 20
    {
        "name"          : "exchange_rate",
        "field_name"    : "Exchange Rate",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "shipment_details",  
        "field_category": "Shipment Details" ,
        "type"          : "default"
    },
    #field_id = 21
    {
        "name"          : "port",
        "field_name"    : "Port",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "shipment_details",  
        "field_category": "Shipment Details" ,
        "type"          : "default"
    },
    #field_id = 22
    {
        "name"          : "vessel",
        "field_name"    : "Vessel",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "shipment_details",  
        "field_category": "Shipment Details" ,
        "type"          : "default"
    },
    #field_id = 23
    {
        "name"          : "voyage",
        "field_name"    : "Voyage",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "shipment_details",  
        "field_category": "Shipment Details" ,
        "type"          : "default"
    },
    #field_id = 24
    {
        "name"          : "sailing_date",
        "field_name"    : "Sailing Date",
        "descp"         : "",
        "dType"         : "Number",
        "category"      : "shipment_details",  
        "field_category": "Shipment Details" ,
        "type"          : "default"
    },
    #field_id = 25
    {
        "name"          : "invoiceparty_name",
        "field_name"    : "Invoice Party Name",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "name_address", 
        "field_category": "Name Address Details" ,
        "type"          : "default"
    },
    #field_id = 26
    {
        "name"          : "invoiceparty_address",
        "field_name"    : "Invoice Party Address",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "name_address", 
        "field_category": "Name Address Details" , 
        "type"          : "default"
    },
    #field_id = 27
    {
        "name"          : "local_amount",
        "field_name"    : "Local Amount",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },
    #field_id = 28
    {
        "name"          : "invoice_currency",
        "field_name"    : "Invoice Currency",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "amount_details",  
        "field_category": "Amount Details" ,
        "type"          : "default"
    },

    #field_id = 29
    {
        "name"          : "container_name",
        "field_name"    : "Container Name",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "container_details",  
        "field_category": "Container Details" ,
        "type"          : "default"
    },

    #field_id = 30
    {
        "name"          : "container_size",
        "field_name"    : "Container Size",
        "descp"         : "",
        "dType"         : "Float",
        "category"      : "container_details",  
        "field_category": "Container Details" ,
        "type"          : "default"
    },

    #field_id = 31
    {
        "name"          : "line_currency",
        "field_name"    : "Line Currency",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    
    #field_id = 32
    {
        "name"          : "amount_in_line_currency",
        "field_name"    : "Amount In Line Currency",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    
    #field_id = 33
    {
        "name"          : "amount_in_invoice_currency",
        "field_name"    : "Amount In Invoice Currency",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 34
    {
        "name"          : "conversion_exchange_rate",
        "field_name"    : "Conversion Exchange Rate",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 35
    {
        "name"          : "amount_in_local_currency",
        "field_name"    : "Amount In Local Currency",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 36
    {
        "name"          : "igst",
        "field_name"    : "IGST",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 37
    {
        "name"          : "cgst",
        "field_name"    : "CGST",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    #field_id = 38
    {
        "name"          : "sgst",
        "field_name"    : "SGST",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",  
        "field_category": "Table Details" ,
        "type"          : "default"
    },
    
    #field_id = 39
    {
        "name"          : "line_notes",
        "field_name"    : "Line Notes",
        "descp"         : "",
        "dType"         : "String",
        "category"      : "table",
        "field_category": "Table Details",
        "type"          : "default"
    }
]

"""
docType_default = [
    #docType_id = 1
    {
        "name"      : "generic_invoice",
        "doc_name"  : "Generic Invoices",
        "descp"     : "",
        "fIds"      : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "type"      : "default"
    },
    #docType_id = 2
    {
        "name"      : "shipment_invoice",
        "doc_name"  : "Shipping Invoices",
        "descp"     : "",
        "fIds"      : [1, 5, 6, 8, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33,34,35,36,37,38,39],
        "type"      : "default"
    }
]
"""

docType_default = [
    #docType_id = 1
    {
        "name"      : "generic_invoice",
        "doc_name"  : "Generic Invoices",
        "descp"     : "",
        "type"      : "default"
    },
    #docType_id = 2
    {
        "name"      : "shipment_invoice",
        "doc_name"  : "Shipping Invoices",
        "descp"     : "",
        "type"      : "default"
    },
    #docType_id = 3
    {
        "name"      : "commercial_invoice",
        "doc_name"  : "Commercial Invoices",
        "descp"     : "",
        "type"      : "default"
    },
    #docType_id = 4
    {
        "name"      : "certificate_of_origin",
        "doc_name"  : "Certificate of Origin",
        "descp"     : "",
        "type"      : "default"
    },
    #docType_id = 5
    {
        "name"      : "bill_of_lading",
        "doc_name"  : "Bill of Lading",
        "descp"     : "",
        "type"      : "default"
    },
    #docType_id = 6
    {
        "name"      : "packing_list",
        "doc_name"  : "Packing List",
        "descp"     : "",
        "type"      : "default"
    }
]

