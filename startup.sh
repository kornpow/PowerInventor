# Default to UTC if no TIMEZONE env variable is set
echo "Setting time zone to ${TIMEZONE=UTC}"
# This only works on Debian-based images
echo "${TIMEZONE}" > /etc/timezone
dpkg-reconfigure tzdata

cd src
#	uncomment for website
# python create_server.py
#	uncomment for particle website
# python particle_server.py
python MAX6675.py



date