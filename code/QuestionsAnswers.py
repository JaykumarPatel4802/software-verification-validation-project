QuestionsAnswers = {
    "How many artists and customers are there?": {
        "SQL_Query": """
                        SELECT
                            (SELECT COUNT(DISTINCT ArtistId) FROM Artist) as ArtistCount,
                            (SELECT COUNT(DISTINCT CustomerId) FROM Customer) as CustomerCount;
                    """,
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
    "What is the first and last name of the customer who spent the most total money, and what was the amount they spent?": {
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
    # "2 What is the first and last name of the customer who spent the most total money, and what was the amount they spent?": {
    #     "SQL_Query": """
    #                     SELECT c.FirstName, c.LastName, SUM(i.Total) as TotalSpent
    #                     From Invoice i
    #                     JOIN Customer c ON i.CustomerId = c.CustomerId
    #                     GROUP BY c.CustomerId, c.FirstName, c.LastName
    #                     ORDER BY TotalSpent DESC
    #                     LIMIT 1;
    #                 """,
    #     "Answer": None
    # },
    "Who is the biggest fan for each artist? In order words, for each artist, which customer bought most of their tracks?": {
        "SQL_Query": """
                        WITH TrackPurchaseCount AS (
                            SELECT 
                                a.ArtistId,
                                i.CustomerId,
                                COUNT(il.TrackId) AS TrackPurchaseCount
                            FROM InvoiceLine il
                            JOIN Invoice i ON il.InvoiceId = i.InvoiceId
                            JOIN Track t ON il.TrackId = t.TrackId
                            JOIN Album al ON t.AlbumId = al.AlbumId
                            JOIN Artist a ON al.ArtistId = a.ArtistId
                            GROUP BY a.ArtistId, i.CustomerId
                        ),
                        RankedFans AS (
                            SELECT 
                                tpc.ArtistId,
                                tpc.CustomerId,
                                tpc.TrackPurchaseCount,
                                RANK() OVER (PARTITION BY tpc.ArtistId ORDER BY tpc.TrackPurchaseCount DESC) AS rnk
                            FROM TrackPurchaseCount tpc
                        )
                        SELECT 
                            a.Name AS ArtistName,
                            r.CustomerId AS BiggestFanCustomerId,
                            r.TrackPurchaseCount AS TracksPurchased
                        FROM RankedFans r
                        JOIN Artist a ON r.ArtistId = a.ArtistId
                        WHERE r.rnk = 1;
                    """,
        "Answer": None
    }
}