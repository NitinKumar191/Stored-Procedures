

CREATE OR ALTER PROCEDURE trial_bases ( @CounterParty NVARCHAR(100) )
AS
Begin

SELECT * FROM [vw_tblinvestment] WHERE Counterparty = 'Borrower AS'

End
