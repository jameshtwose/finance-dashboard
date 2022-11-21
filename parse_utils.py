# plot_color_list = ["#5F4A89", "#4A4453", "#AFA8BA", "#006452", "#009883"]
plot_color_list = ["rgba(91, 22, 106, 1)",
                   "rgba(124, 213, 77, 1)",
                   "rgba(59, 12, 71, 1)",
                   "rgba(138, 12, 184, 1)",
                   "rgba(18, 139, 177, 1)",
                   "rgba(35, 206, 217, 1)",
                   "rgba(35, 128, 15, 1)",
                   "rgba(143, 56, 22, 1)",
                   "rgba(219, 78, 109, 1)",
                   "rgba(84, 12, 34, 1)"]

# ING
ING_DUTCH_columns_list = ['Datum', 'Naam / Omschrijving', 'Rekening', 'Tegenrekening', 'Code',
       'Af Bij', 'Bedrag (EUR)', 'Mutatiesoort', 
       # 'Mededelingen'
       ]

ING_ENGLISH_columns_list = ['Date', 'Name / Description', 'Account', 'Counterparty', 'Code',
       'Debit/credit', 'Amount (EUR)', 'Transaction type', 
       # 'Notifications'
       ]

ING_DUTCH_TO_ENGLISH_dict = dict(zip(ING_DUTCH_columns_list, 
                                     ING_ENGLISH_columns_list))

# ASN
ASN_column_names = ["Boekingsdatum", "Opdrachtgeversrekening",
                "Tegenrekeningnummer", "Naam tegenrekening", "Adres",
                "Postcode", "Plaats", "Valutasoort rekening",
                "Saldo rekening voor mutatie", "Valutasoort mutatie",
                "Transactiebedrag", "Journaaldatum", "Valutadatum",
                "Interne transactiecode", "Globale transactiecode",
                "Volgnummer transactie", "Betalingskenmerk", 
                "Omschrijving", "Afschriftnummer"]

ASN_column_subset = ["Boekingsdatum", "Naam tegenrekening", "Opdrachtgeversrekening", "Tegenrekeningnummer",
                     "Globale transactiecode", "Transactiebedrag", "Saldo rekening voor mutatie"]

ASN_ENGLISH_columns_list = ['Date', 'Name / Description', 'Account', 'Counterparty', 'Code',
                            'Amount (EUR)', 'Total (EUR)']

ASN_DUTCH_TO_ENGLISH_dict = dict(zip(ASN_column_subset, 
                                     ASN_ENGLISH_columns_list))


# BUNQ
BUNQ_column_subset = ['Date', 'Amount', 'Account', 'Counterparty', 'Name']

BUNQ_TO_ING_names_dict = dict(zip(BUNQ_column_subset, ["Date", 'Amount (EUR)', 'Account', 'Counterparty', 'Name / Description']))

# REVOLUT
REVOLUT_column_subset = ['Type', 'Product', 'Started Date', 'Completed Date', 'Description',
       'Amount', 'Fee', 'Currency', 'State', 'Balance']

REVOLUT_column_subset = ['Completed Date', 'Amount', 'Product', 'Description', 'Type']

REVOLUT_TO_ING_names_dict = dict(zip(REVOLUT_column_subset, ["Date", 
                                                             'Amount (EUR)', 
                                                             'Account', 
                                                             'Name / Description', 
                                                             'Debit/credit']))

# REVOLUT - Business
REVOLUT_BUSINESS_column_subset = ['Date started (UTC)', 'Date completed (UTC)', 'ID', 'Type',
       'Description', 'Reference', 'Payer', 'Card number', 'Orig currency',
       'Orig amount', 'Payment currency', 'Amount', 'Fee', 'Balance',
       'Account', 'Beneficiary account number',
       'Beneficiary sort code or routing number', 'Beneficiary IBAN',
       'Beneficiary BIC']

REVOLUT_BUSINESS_column_subset = ['Date completed (UTC)', 'Amount', 'Description', 'Type']

REVOLUT_BUSINESS_TO_ING_names_dict = dict(zip(REVOLUT_BUSINESS_column_subset, ["Date", 
                                                             'Amount (EUR)', 
                                                             'Name / Description', 
                                                             'Debit/credit']))
