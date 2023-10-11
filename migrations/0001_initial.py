from . import AbstractMigration


class Migration(AbstractMigration):
    @classmethod
    def forward(cls):
        operations = (
            """
            CREATE TABLE `migrations` (
                `id` int(4) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
                `name` VARCHAR(37) NOT NULL,
                PRIMARY KEY (`id`), UNIQUE KEY `name` (`name`)
            ) ENGINE=InnoDB
            """
        )
        return operations

    @classmethod
    def backward(cls):
        operations = (
            """
            DROP TABLE `migrations`
            """
        )
        return operations
