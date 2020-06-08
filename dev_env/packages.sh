# install required packages
dnf update -y
dnf install -y python3-sqlalchemy python36 python3-requests python3-psycopg2 python3-tqdm

dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf -qy module disable postgresql
dnf install -y postgresql12-server
