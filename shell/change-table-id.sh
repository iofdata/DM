if [  $# != 3 ]; then
        echo "Usage: sh $0 id table old.sql | sh "
        echo "This script will change the raw sql file directly."
        echo "Please make sure you have a backup for checking!"
        exit
fi

echo cp $3 ${3}.bak

tmp=$(($1 * 8))
table_id=$(($tmp - 7))
new_id=""

while [ $table_id -le $tmp ];do
        if [ $table_id -lt 10 ];then
              new_id="00$table_id"
        elif [ $table_id -lt 100 ];then
             new_id="0$table_id"
        else
            new_id="$table_id"
        fi

        if [ $(($table_id % 8)) == 1 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}001\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 2 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}002\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 3 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}003\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 4 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}004\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 5 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}005\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 6 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}006\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 7 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}007\/${2}$new_id\/ig\' $3
        elif [ $(($table_id % 8)) == 0 ]; then
            echo  "echo $new_id changed"
            echo sed -i \'s\/${2}008\/${2}$new_id\/ig\' $3
        else
            echo "!WRONG!"
        fi

        table_id=$(( $table_id + 1 ))
done