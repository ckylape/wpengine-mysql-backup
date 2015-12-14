WP Engine Database Backups
--------------------------------
This script connects to multiple WP Engine sites over SFTP and downloads the latest MySQL dumps.

### Requirements, Setup, and Usage
The script uses the [Paramiko](http://www.paramiko.org/) library to establish the SFTP connection.

```bash
pip install -r requirements.txt
cp settings.example.json settings.json
python run.py
```

### Settings
Most of the SFTP settings can be found on the Overview page of your site on [my.wpengine.com](http://my.wpengine.com)

- **hostname** - Server IP Address
- **port** - SFTP Port Number
- **username** - SFTP Username (may need created)
- **password** - SFTP User Password (created when the user is)
- **filepath** - The filepath to the `mysql.sql` file, this normally is `wp-content/mysql.sql`
