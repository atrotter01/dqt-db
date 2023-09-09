#find /mnt/d/DQT/gbl/images/ -type f -name "*#*" -exec rm -v {} \;
#find /mnt/d/DQT/ja/images/ -type f -name "*#*" -exec rm -v {} \;
rsync -acv --exclude "*#*" --size-only /mnt/d/DQT/gbl/images/ /home/adam/dqt-db/static/dqt_images/
rsync -acv --exclude "*#*" --size-only /mnt/d/DQT/ja/images/ /home/adam/dqt-db/static/dqt_images/
rsync -acv --size-only /home/adam/dqt-db/static/dqt_images/  bigdracky@41.182.62.50.host.secureserver.net:/home/bigdracky/dqt-db/static/dqt_images/
