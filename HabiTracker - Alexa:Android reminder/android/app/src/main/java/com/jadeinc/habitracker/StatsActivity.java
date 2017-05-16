package com.jadeinc.habitracker;

import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class StatsActivity extends AppCompatActivity {

    public static final String TAG = "StatsActivity";
    private ListView lv;
    private List<Task> taskDisplay;
    private DBDataReceiver receiver;
    private StatsAdapter adapter;
    private User user;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_stats);
        lv = (ListView) findViewById(R.id.lv);
        lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position,
                                    long id) {
                Log.v(TAG, "working");
                Intent intent = new Intent(StatsActivity.this, Adapter.class);
                String message = "abc";
                intent.putExtra(EXTRA_MESSAGE, message);
                startActivity(intent);
            }
        });

        TextView tvDisplayDate0 = (TextView) findViewById(R.id.tvDate0);
        //TextView tvDisplayDate1 = (TextView) findViewById(R.id.tvDate1);
        //TextView tvDisplayDate2 = (TextView) findViewById(R.id.tvDate2);


        Calendar calendar = Calendar.getInstance();
        Date today = calendar.getTime();

        calendar.add(Calendar.DAY_OF_YEAR, 1);
        Date tomorrow = calendar.getTime();
        calendar.add(Calendar.DAY_OF_YEAR, 1);
        Date tomorrowtomorrow = calendar.getTime();

        SimpleDateFormat dateFormat = new SimpleDateFormat("EEEE, MMM dd, yyyy");

        String todayAsString = dateFormat.format(today);
        String tomorrowAsString = dateFormat.format(tomorrow);
        String tomorrowtomorrowAsString = dateFormat.format(tomorrowtomorrow);


        //tvDisplayDate1.setText(tomorrowAsString);
        //tvDisplayDate2.setText(tomorrowtomorrowAsString);
        this.taskDisplay = new ArrayList<Task>();//(Task[]) tasks.toArray();
        adapter = new StatsAdapter(this, taskDisplay);
        lv.setAdapter(adapter);



        //moving to add new task
        ImageButton addNew = (ImageButton) findViewById(R.id.add_task);
        addNew.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(StatsActivity.this, NewTask.class);
                startActivity(i);
            }
        });
    }

    @Override
    public void onResume() {
        super.onResume();
        IntentFilter filter = new IntentFilter(DBDataReceiver.ACTION_RESP);
        filter.addCategory(Intent.CATEGORY_DEFAULT);
        receiver = new DBDataReceiver();
        registerReceiver(receiver, filter);
        Intent dbIntent = new Intent(this, DBService.class);
        startService(dbIntent);
    }

    public void generateTaskList(List<User> users) {
        Log.v(TAG, "got them users");
        user = users.get(0);
        List<Task> tasks = user.getTasks();
        ((StatsAdapter)lv.getAdapter()).updateTasks(tasks);
    }

    public void onTasksClick(View view) {
        Intent myIntent = new Intent(this, HabitList.class);
        startActivity(myIntent);
    }

    public void onAddTaskClick(View view) {
        Intent i = new Intent(this, NewTask.class);
        startActivity(i);
    }

}
