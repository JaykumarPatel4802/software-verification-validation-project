QuestionsAnswers = {
    # Quary type: selection (WHERE)
    "How many artists and customers are there?": {
        "SQL_Query": """
                        SELECT
                            (SELECT COUNT(DISTINCT ArtistId) FROM Artist) as ArtistCount,
                            (SELECT COUNT(DISTINCT CustomerId) FROM Customer) as CustomerCount;
                    """,
        "Answer": None
    },
    # Quary type: window aggregate (GROUP BY + ARRANGE + SLICE)
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
    # Quary type: join (JOIN)
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
    # Quary type: complex
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
    },
    # Quary type: selection (WHERE) 
    "List all the customers' name from TX, USA": {
        "SQL_Query": """
                      SELECT FirstName, LastName FROM Customer WHERE State = 'TX' AND Country = 'USA';
                    """,
        "Answer": None
    },
    # Quary type: conditional selection (CASE WHEN + SELECT) 
    "Get the employees' name and title if they were born before 1965. Get only the name of the rest of the employees": {
        "SQL_Query": """
                      SELECT 
                        CASE
                          WHEN BirthDate < '1965-01-01' 
                          THEN CONCAT(FirstName, ' ', LastName, ' (', Title, ')')
                          ELSE CONCAT(FirstName, ' ', LastName)
                        END AS EmployeeInfo
                      FROM Employee;
                    """,
        "Answer": None
    },
    # Quary type: aggregate (COUNT)
    "How many genres are there?": {
        "SQL_Query": """
                      SELECT COUNT(*) AS GenreCount FROM Genre;
                    """,
        "Answer": None
    },
    # Quary type: aggregate (SUM)
    "What is the sum of total invoices?": {
        "SQL_Query": """
                      SELECT SUM(Total) AS TotalInvoices FROM Invoice;
                    """,
        "Answer": None
    },
    # Quary type: count in group (COUNT + GROUP BY)
    "How many tracks are there in each playlist?": {
        "SQL_Query": """
                      SELECT PlaylistId, COUNT(TrackId) AS TrackCount
                      FROM PlaylistTrack
                      GROUP BY PlaylistId;
                    """,
        "Answer": None
    },
    # Quary type: window aggregate (GROUP BY + ARRANGE + SLICE)
    # ChatGPT got 1/3 tries correct
    "What are the top three longest songs' name for each media_type?": {
        "SQL_Query": """
                      WITH RankedSongs AS (
                        SELECT 
                          m.Name AS MediaTypeName, 
                          t.Name AS TrackName, 
                          t.Milliseconds,
                          ROW_NUMBER() OVER (PARTITION BY m.MediaTypeId ORDER BY t.Milliseconds DESC) AS Rank
                        FROM Track t 
                        INNER JOIN MediaType m ON t.MediaTypeId = m.MediaTypeId
                      )
                      SELECT 
                        MediaTypeName, 
                        TrackName
                      FROM RankedSongs
                      WHERE Rank <= 3;
                    """,
        "Answer": None
    },
    # Quary type: complex
    "Which artist has the most number of songs per album, and how many songs does he have per album?": {
        "SQL_Query": """
                      SELECT 
                        a.ArtistId, ar.Name, 
                        COUNT(t.TrackId) AS SongsPerAlbum
                      FROM Album a
                      JOIN Artist ar ON a.ArtistId = ar.ArtistId
                      JOIN Track t ON a.AlbumId = t.AlbumId
                      GROUP BY a.AlbumId, ar.ArtistId, ar.Name
                      ORDER BY SongsPerAlbum DESC
                      LIMIT 1;
                    """,
        "Answer": None
    },
    # Quary type: complex
    # ChatGPT got 1/3 tries correct
    "Which three countries spend the most money on pop music? How much do they spend, respectively?": {
        "SQL_Query": """
                      SELECT c.Country, SUM(il.UnitPrice * il.Quantity) AS TotalSpent
                      FROM InvoiceLine il
                      JOIN Track t ON il.TrackId = t.TrackId
                      JOIN Album a ON t.AlbumId = a.AlbumId
                      JOIN Artist ar ON a.ArtistId = ar.ArtistId
                      JOIN Invoice i ON il.InvoiceId = i.InvoiceId
                      JOIN Customer c ON i.CustomerId = c.CustomerId
                      WHERE t.GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Pop')
                      GROUP BY c.Country
                      ORDER BY TotalSpent DESC
                      LIMIT 3;
                    """,
        "Answer": None
    },
    # Quary type: complex
    # No correct answer from ChatGPT. Written manually.
    "Which month, when averaging sales from 2009 to 2013, had the highest sales in dollars? How much higher is the average sales for this month compared to the overall average across all months during this period? Please round the result to two decimal places.": {
        "SQL_Query": """
                WITH MonthlySales AS (
                    SELECT 
                        strftime('%m', InvoiceDate) AS Month,  -- Extracts the month (01-12) without the year
                        SUM(Total) AS SalesTotal
                    FROM 
                        Invoice
                    WHERE 
                        strftime('%Y', InvoiceDate) BETWEEN '2009' AND '2013'
                    GROUP BY 
                        Month, strftime('%Y', InvoiceDate) -- Group by both year and month to get sales per month per year
                ),
                AverageMonthlySales AS (
                    SELECT 
                        Month,
                        AVG(SalesTotal) AS AverageSales  -- Computes the average sales for each month across all years
                    FROM 
                        MonthlySales
                    GROUP BY 
                        Month
                ),
                OverallAverage AS (
                    SELECT 
                        AVG(AverageSales) AS OverallAverageSales  -- Computes the overall average across all months
                    FROM 
                        AverageMonthlySales
                )
                SELECT 
                    AMS.Month,
                    ROUND(AMS.AverageSales, 2) AS HighestAverageSales,
                    ROUND(AMS.AverageSales - OA.OverallAverageSales, 2) AS DifferenceFromOverall
                FROM 
                    AverageMonthlySales AMS,
                    OverallAverage OA
                WHERE 
                    AMS.AverageSales = (SELECT MAX(AverageSales) FROM AverageMonthlySales);
                    """,
        "Answer": None
    },
    # Quary type: complex
    # No correct answer from ChatGPT. Written manually.
    "Which playlist has the largest total size in bytes? If my internet speed is 100 MB/s, how long would it take to download that playlist?": {
        "SQL_Query": """
                      SELECT 
                          p.Name, 
                          SUM(t.Bytes) AS TotalSizeBytes,
                          ROUND(SUM(t.Bytes) / (100 * 1024 * 1024), 2) AS DownloadTimeSeconds
                      FROM 
                          Playlist p
                      JOIN 
                          PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId
                      JOIN 
                          Track t ON pt.TrackId = t.TrackId
                      GROUP BY 
                          p.PlaylistId, p.Name
                      ORDER BY 
                          TotalSizeBytes DESC
                      LIMIT 1;
                    """,
        "Answer": None
    },
    
}