# ING
ING_DUTCH_columns_list = ['Datum', 'Naam / Omschrijving', 'Rekening', 'Tegenrekening', 'Code',
       'Af Bij', 'Bedrag (EUR)', 'Mutatiesoort', 'Mededelingen']

ING_ENGLISH_columns_list = ['Date', 'Name / Description', 'Account', 'Counterparty', 'Code',
       'Debit/credit', 'Amount (EUR)', 'Transaction type', 'Notifications']

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