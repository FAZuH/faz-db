from unittest.mock import MagicMock


a = MagicMock()
a.body.guild.name = "Test"
print(a.body.guild.name)

