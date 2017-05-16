package com.jadeinc.habitracker;

/**
 * Created by ali on 4/24/17.
 */
import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

import java.util.List;

public class Adapter extends BaseAdapter {
        private List<Task> tasks;
        private Context context;

        public Adapter(Context mcontext, List<Task> t) {
            context = mcontext;
            tasks = t;
        }

        @Override
        public int getCount() {
            try {
                int size = tasks.size();
                return size;
            } catch(NullPointerException o) {
                return 0;
            }
        }

        public void updateTasks(List<Task> t) {
            tasks.clear();
            tasks.addAll(t);
            this.notifyDataSetChanged();
        }

        @Override
        public Task getItem(int i) {
            try {
                Task t = tasks.get(i);
                return t;
            } catch (NullPointerException e) {
                return null;
            }
        }

        @Override
        public long getItemId(int i) {
            return 0;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            LayoutInflater inflater = ((Activity)context).getLayoutInflater();
            convertView = inflater.inflate(R.layout.task_row, parent, false);
            TextView name = (TextView) convertView.findViewById(R.id.textView1);
            CheckBox cb = (CheckBox) convertView.findViewById(R.id.checkBox1);
            cb.setTag(tasks.get(position).getTask());
            name.setText(tasks.get(position).getTask());
            if(tasks.get(position).isCompleted()) {
                cb.setChecked(true);
            } else {
                cb.setChecked(false);
            }
            Button deleteButton = (Button) convertView.findViewById(R.id.deleteHabit);
            deleteButton.setTag(tasks.get(position).getTask());
            return convertView;
        }
}
