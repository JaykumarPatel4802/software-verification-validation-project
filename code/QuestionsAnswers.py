QuestionsAnswers = {
    "How many distinct artists are there?": {
        "SQL_Query": "SELECT COUNT(DISTINCT ArtistId) as DistinctArtists FROM Artist;",
        "Answer": None
    },
    "What are the top 5 countries with the most Invoices?": {
        "SQL_Query": """
                        SELECT BillingCountry,
                            COUNT(InvoiceId) as invoice_count
                        FROM Invoice
                        GROUP BY BillingCountry
                        ORDER BY invoice_count DESC
                        LIMIT 5
                    """,
        "Answer": None
    },
    "What is the first and last name of the customer who spent the most money (summed across all of their invoices), and what was the amount they spent?": {
        "SQL_Query": """
                        WITH CustomerSpending AS (
                            SELECT
                                i.CustomerId,
                                SUM(i.Total) as total_spent
                            FROM Invoice i
                            GROUP BY i.CustomerId
                        )
                        SELECT c.FirstName, c.LastName, cs.total_spent
                        FROM CustomerSpending cs
                        JOIN Customer c on cs.CustomerId = c.CustomerId
                        WHERE cs.total_spent = (SELECT MAX(total_spent) from CustomerSpending);
                    """,
        "Answer": None
    },
    "2 What is the first and last name of the customer who spent the most money (summed across all of their invoices), and what was the amount they spent?": {
        "SQL_Query": """
                        SELECT c.FirstName, c.LastName, SUM(i.Total) as TotalSpent
                        From Invoice i
                        JOIN Customer c ON i.CustomerId = c.CustomerId
                        GROUP BY c.CustomerId, c.FirstName, c.LastName
                        ORDER BY TotalSpent DESC
                        LIMIT 1;
                    """,
        "Answer": None
    }
}