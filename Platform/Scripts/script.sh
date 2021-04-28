echo "[1/6] Setting Home Directory..."
cd AIRMON-Platform-V2/Platform/
echo "[2/6] Stopping Docker Compose..."
sudo docker-compose stop
cd ..
echo "[3/6] Backing up Database..."
sudo docker exec AIRMON_database pg_dumpall -c -U admin > BACKUPS/dump_$(date + "%Y-%m-%d_%H_%M_%S")_AUTO.sql
echo "[4/6] Retrieving lastest git..."
git checkout master
git reset --hard origin/master
cd Platform/Frontend
echo "[5/6] Building Frontend outside docker (memmory limitations)..."
sudo npm run build
cd ..
echo "[6/6] Running Docker Compose..."
sudo docker-compose build --force-rm --no-cache
sudo docker-compose up