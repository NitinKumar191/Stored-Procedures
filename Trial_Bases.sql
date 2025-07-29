

CREATE OR ALTER PROCEDURE trial_bases ( @CounterParty NVARCHAR(100) )
AS
Begin

SELECT * FROM [vw_tblinvestment] WHERE Counterparty = 'Borrower AS' 
and Currency = 'GBP' and LoanID = '80af18da-7e9d-4f9d-abcc-66c4649b1c62'

End
