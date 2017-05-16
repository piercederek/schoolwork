package com.jadeinc.habitracker;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by evan on 4/25/17.
 */
public class DBDataReceiver extends BroadcastReceiver {
    public static final String ACTION_RESP =
            "com.jadeinc.habitracker.DATA_REC";

    public static List<User> users;

    @Override
    public void onReceive(Context context, Intent intent) {
        List<Task> tasks = users.get(0).getTasks();  //new ArrayList();//DBConnector.users.get(0).getTasks();
        if(context instanceof HabitList) {
            ((HabitList) context).generateTaskList(users);
        } else if (context instanceof StatsActivity) {
            ((StatsActivity) context).generateTaskList(users);
        }
        Log.v("DBReceiver", intent.getAction());
    }

}