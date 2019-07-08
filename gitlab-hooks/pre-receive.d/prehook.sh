#!/bin/bash

LOGFILE="/var/log/gitlab/diluhook/prehook.log"
function log()
{
  echo "$@" >> $LOGFILE
}

echo "================================================"
echo "Say Hi From Dilusense Gitlab Server." 
echo "1. check code style "
echo "2. check comment style ...etc."

#exit 0


read OLD_VALUE NEW_VALUE BRANCH

log ""
log ""
log ">>>>>>>>>>>>>>>>>"`date`"<<<<<<<<<<<<<<<<<<"


# project which kuangch created do not check
matched=`pwd |grep /var/opt/gitlab/git-data/repositories/kuangch |wc -l`
if [ $matched -eq 1 ];
then
  log "kuangch 不检测"
  exit 0
fi


log "Read Params:" $OLD_VALUE $NEW_VALUE $BRANCH 
log "Git log as below"
git log ${OLD_VALUE}..${NEW_VALUE} --pretty="%B" >> $LOGFILE 2>&1
log "Git log DONE" 


if [ $OLD_VALUE = "0000000000000000000000000000000000000000" -o $NEW_VALUE = "0000000000000000000000000000000000000000" ] ;
then
  log "drop branch or new branch or just add a new file "
  exit 0
fi

FLAG=0

# check comments
comments=`git log ${OLD_VALUE}..${NEW_VALUE} --pretty="DILUCOMMENTS:%B" |grep -v "^$"`

log ""
log "check comment one bye one " 
log "$comments" 

count=0
line=`echo "$comments" |sed -n '/DILUCOMMENTS:/=' `
cnt=`echo "$comments" | wc -l`
line=`echo $line $(expr $cnt + 1)`
startLine=1


for n in ${line}
do
   if [ $count -eq 0 ] ; then
     let count+=1
     continue
   fi
   let endLine=n-1
   comm=`echo "$comments" | sed -n "${startLine},${endLine}p" | sed 's/DILUCOMMENTS://' `

   echo ""
   echo "$comm" 
   ret1=`echo "$comm"|grep ^bug\ id:` 
   ret2=`echo "$comm"|grep ^desc:`
   ret3=`echo "$comm"|grep ^tests:`
   ret4=`echo "$comm"|grep ^task\ id:`

   if [ "$ret1" = "" -o "$ret2" = "" -o "$ret3" = "" -o "$ret4" = "" ] ;
   then
      echo "$comm" | awk '{print $1}' |grep "^#[0-9]*$" >> /dev/null
      if [ $? -eq 0 ] ;
      then
        log "issue updated"
        echo "issue updated"
      else 
        echo "$comm" | grep "^Merge branch" >> /dev/null
        if [ $? -eq 0 ] ;
        then
          log "Merge branch"
          echo "Merge branch"
        else 
          log "格式错误:" "$comm"
          echo -e "格式错误:\n" "$comm"
          echo "提交Comments格式有误，请严格按照如下格式"
          echo "    bug id:001"
          echo "    task id:001"
          echo "    time:8 (可选)"
          echo "    done (可选)"
          echo "    desc:此次提交的描述"
          echo "    tests:为此次提交做过的测试"
          exit 1
        fi
      fi
   fi

   startLine=$n
done


echo "******************"
if [ $FLAG -eq 0 ]
then
    echo "√  代码检查通过."
else
    echo "×  代码检查不通过!请酌情处理！"
fi

echo "================================================"
exit 0
