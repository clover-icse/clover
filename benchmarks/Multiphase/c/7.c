int main(){
    int x, y, z, v;

    // pre-conditions
    assume(x > y);
    assume(y > z);
    v = 0;

    // loop body
    while(unknown()){
        if(x < y){
            v = v + 1;
        }
        x = x + 1;
        y = y + 3;
        z = z + 2;
        
    }

    // post-condition
    if((z - x) > 72531){
        assert(v > 0);
    }
    
}