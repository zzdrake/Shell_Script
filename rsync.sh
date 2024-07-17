SOURCE_USER="username"
SOURCE_HOST="ipaddr"
SOURCE_DIR="ssh_path"
DEST_DIR="local_path"

rsync -avz --ignore-existing --delete -e "ssh -o StrictHostKeyChecking=no" $SOURCE_USER@$SOURCE_HOST:$SOURCE_DIR $DEST_DIR