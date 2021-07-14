
if ( $# == 0 )
  then
    echo "passer le nom du user a creer en parametre"
fi

username="$1"
first_name="${username}"
last_name="${username}"
email="${username}.${username}@awx.com"
password="${username}"


input="{username:${username},first_name:${first_name},last_name:${last_name},email:${email},password:${username}}"

curl -XPOST -u admin -H "Content-Type:application/json" -d "{\"username\":\"${username}\",\"first_name\":\"${first_name}\",\"last_name\":\"${last_name}\",\"email\":\"${email}\",\"password\":\"${username}\"}" http://localhost/api/v2/users/
