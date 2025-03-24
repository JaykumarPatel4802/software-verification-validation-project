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
    # "Get the employees' name and title if they were born before 1965. Get only the name of the rest of the employees": {
    #     "SQL_Query": """
    #                   SELECT 
    #                     CASE
    #                       WHEN BirthDate < '1965-01-01' 
    #                       THEN CONCAT(FirstName, ' ', LastName, ' (', Title, ')')
    #                       ELSE CONCAT(FirstName, ' ', LastName)
    #                     END AS EmployeeInfo
    #                   FROM Employee;
    #                 """,
    #     "Answer": None
    # },
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


Bird_QuestionsAnswers = {
    # Simple
    "What's Angela Sanders's major?": {
        "SQL_Query": "SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Angela' AND T1.last_name = 'Sanders'",
        "Answer": None
    },
    "How many students in the Student_Club are from the College of Engineering?": {
        "SQL_Query": "SELECT COUNT(T1.member_id) FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.college = 'College of Engineering'",
        "Answer": None
    },
    "Please list the full names of the students in the Student_Club that come from the Art and Design Department.": {
        "SQL_Query": "SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.department = 'Art and Design Department'",
        "Answer": None
    },
    "How many students of the Student_Club have attended the event \"Women's Soccer\"?": {
        "SQL_Query": "SELECT COUNT(T1.event_id) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'Women''s Soccer'",
        "Answer": None
    },
    "What is the event that has the highest attendance of the students from the Student_Club?": {
        "SQL_Query": "SELECT T1.event_name FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event GROUP BY T1.event_name ORDER BY COUNT(T2.link_to_event) DESC LIMIT 1",
        "Answer": None
    },
    "Which college is the vice president of the Student_Club from?": {
        "SQL_Query": "SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position LIKE 'vice president'",
        "Answer": None
    },
    "Please list the event names of all the events attended by Maya Mclean.": {
        "SQL_Query": "SELECT T1.event_name FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T3.first_name = 'Maya' AND T3.last_name = 'Mclean'",
        "Answer": None
    },
    # Manually Added:
    # "What is the email of Trent Smith?": {
    #     "SQL_Query": "SELECT T1.email FROM member AS T1 WHERE T1.first_name = 'Trent' AND T1.last_name = 'Smith'",
    #     "Answer": None
    # },
    # "List all unique event locations.": {
    #     "SQL_Query": "SELECT DISTINCT T1.location FROM event AS T1",
    #     "Answer": None
    # },
    # "How many different colleges are represented in the Student_Club?": {
    #     "SQL_Query": "SELECT COUNT(DISTINCT T1.college) FROM major AS T1 WHERE T1.major_id IN (SELECT T2.link_to_major FROM member AS T2)",
    #     "Answer": None
    # },
    # "What are the names of members who have no recorded phone number?": {
    #     "SQL_Query": "SELECT T1.first_name, T1.last_name FROM member AS T1 WHERE T1.phone IS NULL",
    #     "Answer": None
    # },
    # "How many members have attended at least one event?": {
    #     "SQL_Query": "SELECT COUNT(DISTINCT T1.link_to_member) FROM attendance AS T1",
    #     "Answer": None
    # },
    
    # Moderate
    "Please list the phone numbers of the students from the Student_Club that has attended the event \"Women's Soccer\".": {
        "SQL_Query": "SELECT T3.phone FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T1.event_name = 'Women''s Soccer'",
        "Answer": None
    },
    "Among the students from the Student_Club who attended the event \"Women's Soccer\", how many of them want a T-shirt that's in medium size?": {
        "SQL_Query": "SELECT COUNT(T3.member_id) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T1.event_name = 'Women''s Soccer' AND T3.t_shirt_size = 'Medium'",
        "Answer": None
    },
    "How many events of the Student_Club did Sacha Harrison attend in 2019?": {
        "SQL_Query": "SELECT COUNT(T1.event_id) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T3.first_name = 'Sacha' AND T3.last_name = 'Harrison' AND SUBSTR(T1.event_date, 1, 4) = '2019'",
        "Answer": None
    },
    "Among the events attended by more than 10 members of the Student_Club, how many of them are meetings?": {
        "SQL_Query": "SELECT T1.event_name FROM event AS T1  INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event GROUP BY T1.event_id  HAVING COUNT(T2.link_to_event) > 10 EXCEPT SELECT T1.event_name  FROM event AS T1  WHERE T1.type = 'Meeting'",
        "Answer": None
    },
    "List all the names of events that had an attendance of over 20 students but were not fundraisers.": {
        "SQL_Query": "SELECT T1.event_name FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event GROUP BY T1.event_id HAVING COUNT(T2.link_to_event) > 20 EXCEPT SELECT T1.event_name FROM event AS T1  WHERE T1.type = 'Fundraiser'",
        "Answer": None
    },
    # Manually Added:
    # "List the names of members who have incurred an approved expense.": {
    #     "SQL_Query": "SELECT DISTINCT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T2.approved = 'true'",
    #     "Answer": None
    # },
    # "How many members attended at least one event in 2022?": {
    #     "SQL_Query": "SELECT COUNT(DISTINCT T2.link_to_member) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE SUBSTR(T1.event_date, 1, 4) = '2022'",
    #     "Answer": None
    # },
    # "How many events have had at least 20 attendees?": {
    #     "SQL_Query": "SELECT COUNT(T1.event_id) FROM (SELECT T2.link_to_event, COUNT(T2.link_to_member) as num_attendees FROM attendance AS T2 GROUP BY T2.link_to_event HAVING num_attendees >= 20) AS subquery",
    #     "Answer": None
    # },
    # "List the emails of members who attended the most recent event.": {
    #     "SQL_Query": "SELECT DISTINCT T1.email FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member WHERE T2.link_to_event = (SELECT T3.event_id FROM event AS T3 ORDER BY T3.event_date DESC LIMIT 1)",
    #     "Answer": None
    # },
    
    # Challenging
    "Calculate the total average cost that Elijah Allen spent in the events on September and October.": {
        "SQL_Query": "SELECT AVG(T2.cost) FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T1.last_name = 'Allen' AND T1.first_name = 'Elijah' AND (SUBSTR(T2.expense_date, 6, 2) = '09' OR SUBSTR(T2.expense_date, 6, 2) = '10')",
        "Answer": None
    },
    "How many times was the budget in Advertisement for \"Yearly Kickoff\" meeting more than \"October Meeting\"?": {
        "SQL_Query": "SELECT CAST(SUM(CASE WHEN T2.event_name = 'Yearly Kickoff' THEN T1.amount ELSE 0 END) AS REAL) / SUM(CASE WHEN T2.event_name = 'October Meeting' THEN T1.amount ELSE 0 END) FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.category = 'Advertisement' AND T2.type = 'Meeting'",
        "Answer": None
    },
    "What is the name of the social event that was attended by the vice president of the Student_Club located at 900 E. Washington St.?": {
        "SQL_Query": "SELECT T2.event_name FROM attendance AS T1 INNER JOIN event AS T2 ON T2.event_id = T1.link_to_event INNER JOIN member AS T3 ON T1.link_to_member = T3.member_id WHERE T3.position = 'Vice President' AND T2.location = '900 E. Washington St.' AND T2.type = 'Social'",
        "Answer": None
    },
    # Manually Added:
    # "Which event had the highest total expense?": {
    #     "SQL_Query": "SELECT T2.event_name, SUM(T1.cost) AS total_expense FROM expense AS T1 INNER JOIN event AS T2 ON T1.link_to_budget IN (SELECT T3.budget_id FROM budget AS T3 WHERE T3.link_to_event = T2.event_id) GROUP BY T2.event_name ORDER BY total_expense DESC LIMIT 1",
    #     "Answer": None
    # },
    # "Find the member who attended the most events.": {
    #     "SQL_Query": "SELECT T1.first_name, T1.last_name, COUNT(T2.link_to_event) AS event_count FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member GROUP BY T1.member_id ORDER BY event_count DESC LIMIT 1",
    #     "Answer": None
    # },
    # "Which zip code has the most members?": {
    #     "SQL_Query": "SELECT T1.zip, COUNT(*) AS member_count FROM member AS T1 GROUP BY T1.zip ORDER BY member_count DESC LIMIT 1",
    #     "Answer": None
    # },
    # "Calculate the total amount spent on social events in the last two years.": {
    #     "SQL_Query": "SELECT SUM(T1.spent) FROM budget AS T1 WHERE T1.link_to_event IN (SELECT T2.event_id FROM event AS T2 WHERE T2.type = 'Social' AND T2.event_date >= DATE('now', '-2 years'))",
    #     "Answer": None
    # }
    # "List the members who have attended all events.": {
    #     "SQL_Query": "SELECT T1.first_name, T1.last_name FROM member AS T1 WHERE NOT EXISTS (SELECT T2.event_id FROM event AS T2 EXCEPT SELECT T3.link_to_event FROM attendance AS T3 WHERE T3.link_to_member = T1.member_id)",
    #     "Answer": None
    # }
}
